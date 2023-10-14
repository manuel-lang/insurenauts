from api.models import EmailBody, InsurancePackage, CompletionResult
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
import os


def send_email(body: EmailBody) -> dict[str, str]:
    """Send an email as defined in EmailBody"""
    msg = MIMEText(body.message)
    msg["subject"] = body.subject
    with SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(
            os.environ.get("SMTP_EMAIL_ADDRESS", ""),
            os.environ.get("SMTP_PASSWORD", ""),
        )
        smtp_server.sendmail(
            os.environ.get("SMTP_EMAIL_ADDRESS", ""), [body.to], msg.as_string()
        )
    return {"message": "Email sent successfully"}


def get_all_insurance_packages() -> list[InsurancePackage]:
    vehicle_insurace = InsurancePackage(
        name="KFZ",
        price=7,
        description="""
Leistungen:
    - Abdeckung von Fahrzeugunfälle
    - Schutz vor Diebstahl und Schäden des KFZ
    - Unfälle und Pannenhilfe unterstützen

Eine KFZ-Versicherung (Kraftfahrzeugversicherung) schützt den
Versicherungsnehmer vor finanziellen Verlusten und Haftung im 
Zusammenhang mit einem Auto.
                """,
        covered_items=["Vehicle"],
    )

    occupational_disability_instance = InsurancePackage(
        name="Berufsunfaehigkeits",
        price=6,
        description="""
Leistungen:
    - Finanzielle Leistungen bei Berufsunfähigkeit
    - Unterstützung des Lebensunterhalts
    - Sicherung des Einkommens
    
Die Berufsunfähigkeitsversicherung (BU-Versicherung) bietet finanziellen Schutz,
wenn eine Person aufgrund von Krankheit oder Verletzung nicht mehr in der Lage ist,
ihren Beruf auszuüben.
            """,
        covered_items=[
            "Lebenssituation",
            "Lebenslage",
        ],
    )

    household_insurace = InsurancePackage(
        name="Hausrats",
        price=4,
        description="""
Leistungen:
    - Entschädigung von Schäden oder Verlusten im privaten Haushalt 
    - Schützt vor Naturkatastrophen und Feuer

Die Hausratsversicherung schützt den persönlichen Besitz und die Einrichtung in einem
Privathaushalt. Sie deckt Schäden order Verluste, die durch verschiedene versicherte
Ereignisse verursacht werden, wie beispielsweise Diebstahl, Feuer, 
Wasser- oder Sturmschäden.
            """,
        covered_items=["Haustiere", "Lebenslage", "Handy", "Familienstand"],
    )

    abroad_travel_insure = InsurancePackage(
        name="Auslandsreise",
        price=3,
        description="""
Leistungen:
    - Behandlungskosten im Ausland
    - notwendige Medikamente und Verbandsmaterial
    - Krankenrücktransport
    - Such-, Rettungs- und Bergungskosten

Eine Auslandsreiseversicherung bietet Schutz, wenn Sie ins Ausland reisen.
Sie deckt eine Reihe von unerwarteten Situationen und Notfällen, die während
einer Reise auftreten können.
            """,
        covered_items=["Lebenslage", "Reise"],  # TODO ADD ME
    )

    liability_insurance = InsurancePackage(
        name="Haftpflicht",
        price=5,
        description="""
Leistungen:
    - Deckung gegen Schadenersatzansprüche Dritter
    - Schutz vor Haftungsansprüchen

Die Haftpflichtversicherung schützt den Versicherungsnehmer vor finanziellen
Ansprüchen Dritter, die aus Verletzungen oder Schäden resultieren, für die der 
Versicherungsnehmer rechtlich verantwortlich gemacht wird.
            """,
        covered_items=["Lebenssituation", "Lebenslage", "Haustiere"],
    )

    return [
        abroad_travel_insure,
        household_insurace,
        liability_insurance,
        occupational_disability_instance,
        vehicle_insurace,
    ]


def generate_email_content(completion_result: CompletionResult) -> str:
    email_message = """
Lieber Kollege,

Eine weitere Simulation in InsureNauts wurde erfolgreich durchlaufen.

Angaben zur Person:
- Name: {0}
- Email Adresse: {1}

Ermittelte Interessen im Rahmen der Simulation:
- {2}

Durch die automatisierte Auswertung wurden diese Versicherungen als
besonders erfolgsversprächend eingestuft:
- {3}

Mit freundlichen Grüßen,
Ihr InsureNauts Team
    """.format(
        completion_result.name,
        completion_result.email,
        "\n- ".join(completion_result.relevant_attributes),
        "\n- ".join(completion_result.suggested_insurance_packages),
    )

    return email_message
