from dataclasses import dataclass


@dataclass
class ReqCreateUser:
    OpenId: str

@dataclass
class ReqCreateWallet:
    OpenId: str
    ChainID: str

@dataclass
class ReqGetWalletAddr:
    OpenId: str
    ChainIDs: str

@dataclass
class ReqWithdrawByOpenID:
    OpenId: str
    TokenId: str
    Amount: str
    AddressTo: str
    CallBackUrl: str
    SafeCheckCode: str



