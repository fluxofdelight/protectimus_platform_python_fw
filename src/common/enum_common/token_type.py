class SoftwareTokens:
    SMART = "PROTECTIMUS_SMART"
    SMS = "SMS"
    MAIL = "MAIL"
    BOT = "PROTECTIMUS_BOT"
    PUSH = "PUSH"
    GOOGLE = "GOOGLE_AUTHENTICATOR"


class HardwareTokens:
    SHARK = "SHARK"
    TWO = "PROTECTIMUS_TWO"
    FLEX = "FLEX"
    SLIM = "PROTECTIMUS_SLIM"
    SLIM_MINI = "PROTECTIMUS_SLIM_MINI"
    ULTRA = "PROTECTIMUS_ULTRA"


class TokenType:
    software = SoftwareTokens()
    hardware = HardwareTokens()
    universal = "UNIFY_OATH_TOKEN"
