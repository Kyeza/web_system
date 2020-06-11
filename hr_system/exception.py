class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NoEmployeeInSystemError(Error):
    """Exception raised for errors while trying to process payroll period with no employee in the system."""

    def __init__(self, message='Payroll Center has no Employees', line_number=None):
        self.message = message
        self.line_number = line_number


class NoEmployeeInPayrollPeriodError(Error):
    """Exception raised for errors while trying to process payroll period with no employee in the Payroll Processor for
    a particular payroll period."""

    def __init__(self, message='No Employees in current Payroll Process table for this Payroll period',
                 payroll_period=None, line_number=None):
        self.payroll_period = payroll_period
        if self.payroll_period is not None:
            self.message = message.replace('Payroll period', self.payroll_period)
        else:
            self.message = message
        self.line_number = line_number


class ProcessingDataError(Error):
    """Exception raised for errors while processing payroll.

    Attributes:
        exception -- input expression in which the error occurred
        user -- explanation of the error
    """

    def __init__(self, user, exception=None, line_number=None):
        self.user = user
        self.exception = exception
        self.line_number = line_number


class EmptyPAYERatesTableError(Error):
    """Exception raised for errors while the PAYE rates table is empty."""

    def __init__(self, message='PAYE table is empty', line_number=None):
        self.message = message
        self.line_number = line_number


class EmptyLSTRatesTableError(Error):
    """Exception raised for errors while the LST rates table is empty."""

    def __init__(self, message='LST table is empty', line_number=None):
        self.message = message
        self.line_number = line_number
