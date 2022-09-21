import os
import dotenv

dotenv.load_dotenv()

if os.getenv("STAGE") == "DEVELOPMENT":
    SERVER_ID=930385265120387083

    ADMIN_ID=1021747432209535077
    JR_ADMIN_ID=1021768287656366170
    MOD_ID=1021768264352796743
    JR_MOD_ID=1021768220899811391
    
    INVITE_CHANNEL=930385265707610125

    TOTAL_MEMBERS_ID=1022091178960769044

    SERVER_MEMBERS_ID=1022091241233596446


    GUILDS = {
        "SB Uni": {
            "uuid":"6111fcb48ea8c95240436c57",
            "vc": "1022088713267839056"
        },
        "SB Alpha Psi": {
            "uuid": "604a765e8ea8c962f2bb3b7a",
            "vc": "1022088877172863056"
        },
        "SB Kappa Eta": {
            "uuid": "607a0d7c8ea8c9c0ff983976",
            "vc": "1022089074401615932"
        },
        "SB Delta Omega": {
            "uuid": "608d91e98ea8c9925cdb91b7",
            "vc": "1022089218480160871"
        },
        "SB Lambda Pi": {
            "uuid": "60a16b088ea8c9bb7f6d9052",
            "vc": "1022089413590790264"
        },
        "SB Rho Xi": {
            "uuid": "6125800e8ea8c92e1833e851",
            "vc": "1022090892322017321",
        },
        "SB Masters": {
            "uuid": "570940fb0cf2d37483e106b3",
            "vc": "1022091325186781244"
        }
    }
