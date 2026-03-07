from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer, HRFlowable

from app.modules.account.account import Account
from app.modules.account.exceptions import *
from app.modules.account.repository import AccountRepository
from app.modules.account.rule import AccountRules
from app.modules.account.schema import AccountRequest, TransactionRequest, TransactionType

class AccountService:

    def __init__(self, repo: AccountRepository):
        self._repo= repo

    def find_by_num_account(self, num_account: str) -> Account:
        return  self._repo.find_by_num_account(num_account=num_account)

    def create_account(self, account_req: AccountRequest) -> Account:
        self._validate_account_request(account_req)
        user_identity = account_req.user_identity
        existing = self._repo.find_by_user_identity(
            user_identity=user_identity)
        self._validate_existing_account(existing)

        account = Account(
            amount=account_req.amount,
            user_identity=account_req.user_identity
        )
        account = self._repo.save(account)
        self._validate_not_existing_account(account)

        num_account = self._generate_account_number(
            branch=account_req.branch.upper(),
            type_account=account_req.type_account.upper(),
            sequence=account.id
        )
        account.assign_num_account(num_account)
        return self._repo.save(account)

    def transaction(self, transaction_req: TransactionRequest):

        if transaction_req.amount % 10 != 0:
            raise ValueError("El monto debe terminar en 0")

        account = self._repo.find_by_num_account(transaction_req.num_account)
        self._validate_not_existing_account(account)
        amount = transaction_req.amount
        match transaction_req.transaction_type:
            case TransactionType.DEPOSIT:
                account.deposit(amount)
            case TransactionType.WITHDRAW:
                account.withdraw(amount)

        return self._repo.save(account)

    def statement(self, num_account):
        account = self._repo.find_by_num_account(num_account=num_account)
        self._validate_not_existing_account(account)
        return self._generate_extract_pdf(account=account)

    def _generate_extract_pdf(self, account: Account):

        buffer = BytesIO()
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Estado de cuenta", styles['Title']))
        elements.append(Spacer(1, 20))

        elements.append(Paragraph("Número de cuenta: " + account.num_account, styles['Normal']))
        elements.append(Paragraph("Saldo actual: " + str(account.amount), styles['Normal']))
        elements.append(Paragraph("Fecha apertura: " + str(account.register_date), styles['Normal']))

        elements.append(Spacer(1, 10))

        elements.append(HRFlowable(width="100%", thickness=1))
        elements.append(HRFlowable(width="100%"))
        elements.append(Spacer(1, 15))

        data = [["Fecha", "Monto", "Balance"]]
        for e in account.extracts:
            data.append([
                e.register_date.strftime("%Y-%m-%d %H:%M:%S"),
                str(e.amount),
                str(e.balance)
            ])

        table = Table(data, colWidths=["33%", "33%", "34%"])
        elements.append(table)
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        pdf.build(elements)
        buffer.seek(0)

        return buffer

    def _validate_account_request(self, account_req: AccountRequest):
        self._illegal_argument(account_req.type_account, "Type account ")
        self._illegal_argument(account_req.branch, "Branch")
        self._illegal_argument(account_req.user_identity, "User identity")
        self._validate_amount(account_req.amount)

    def _illegal_argument(self, value: str, message: str):
        if value is None or not value.strip():
            raise IllegalArgumentAccountException(
                f"{message} is required"
            )

    def _validate_amount(self, amount: float):
        if amount < AccountRules.MIN_INITIAL_AMOUNT:
            raise InvalidInitialAmountException(
                f"Initial amount must be at least {AccountRules.MIN_INITIAL_AMOUNT}"
            )
        if amount > AccountRules.MAX_INITIAL_AMOUNT:
            raise InvalidInitialAmountException(
                f"Initial amount must be less than {AccountRules.MAX_INITIAL_AMOUNT}"
            )

    def _validate_existing_account(self, account: Account):
        if account is not None:
            raise AccountAlreadyExistsException("Account existing")

    def _validate_not_existing_account(self, account: Account):
        if account is None:
            raise AccountNotAlreadyExistsException("Account not existing")

    def _generate_account_number(
        self,
        branch: str,
        type_account: str,
        sequence: int
    ) -> str:

        numeric_part = f"{sequence:08d}"
        check_digit = self._calculate_luhn(numeric_part)
        return f"{branch}{type_account}{numeric_part}{check_digit}"

    def _calculate_luhn(self, numeric_part: str) -> int:
        total = 0
        alternate = False

        for digit in reversed(numeric_part):
            n = int(digit)

            if alternate:
                n *= 2
                if n > 9:
                    n -= 9

            total += n
            alternate = not alternate

        return (10 - (total % 10)) % 10