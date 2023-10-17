from api.models import (
    EmailBody,
    InsurancePackage,
    CompletionResult,
    Story,
    ChapterNode,
    DoorNode,
    EventNode,
)
from smtplib import SMTP_SSL
from random import shuffle
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


def get_vacation_story_tree() -> ChapterNode:
    """
    Vacation Storyline
    """

    additional_info = """
Wusstest du, dass jeder fünfte Mensch in Deutschland im Urlaub krank wird? 
Dieses Phänomen ist so präsent, dass es auch mit der Leisure Sickness 
beschrieben wird.
"""

    vacation_chapter = ChapterNode(
        text="Du fliegst in der Urlaub nach Italien.",
    )
    vacation_door = DoorNode(
        text="Wähle eine Option!",
    )

    vacation_bad_event1 = EventNode(
        insurance="Auslandsreise",
        costs=4,
        text="""
Nach einem Tag am Strand bemerkst du abends schreckliche Kopfschmerzen. 
Nachdem du extra früher schlafen gegangen bist, hat es sich nicht gebessert 
und du merkst, dass es immer schlimmer wird. Du beschließt, einen Arzt aufzusuchen, 
der eine Grippe diagnostiziert.
Du musst 8 Nautis für diesen Arztbesuch bezahlen und dein Urlaub ist nun gar 
nicht mehr entspannend. (-8)
        """,
        additional_info=additional_info,
    )

    vacation_bad_event2 = EventNode(
        insurance="Auslandsreise",
        costs=10,
        text="""
Im Urlaub wirst du auf ein lokales Restaurant aufmerksam und beschließt, 
trotz erster Skepsis einen Teller mit scheinbar frischen Nudeln und 
Meeresfrüchten zu essen. Später im Hotel wird dir auf einmal übel und 
der Krankenwagen muss dich abholen kommen. 
Es wird eine Lebensmittelvergiftung festgestellt.
Da du keine Auslandskrankenversicherung hast, musst du nun nicht nur gesund werden, 
sondern auch noch die Kosten der Krankenversorgung übernehmen. (-10)
        """,
        additional_info=additional_info,
    )

    vacation_good_event = EventNode(
        insurance="Auslandsreise",
        costs=-2,
        text="""
Du entdeckst deine leidenschaft zum Schnorcheln
Du findest einen kleinen Schatz.
        """,
        additional_info=additional_info,
    )

    possibility_to_insure = ChapterNode(
        insurance="Auslandsreise",
        text="""

""",
        costs=0,
    )

    vacation_bad_event1.next_node = possibility_to_insure
    vacation_bad_event2.next_node = possibility_to_insure

    vacation_door.options = [
        vacation_bad_event1,
        vacation_bad_event2,
        vacation_good_event,
    ]

    shuffle(vacation_door.options)

    vacation_chapter.options = [vacation_door]

    return vacation_chapter


def get_liability_chapter() -> ChapterNode:

    additional_info = """
Die Haftpflichtversicherung ist die beliebteste Versicherung in Deutschland. 
Über 80% der Deutschen sind haftpflichtversichert - und das aus gutem Grund! 
Im Schadensfall können schnell mehrere Tausend Euro fällig werden."""

    """Liability Cover"""
    liability_chapter = ChapterNode(
        insurance="Haftpflicht",
        text="""

""",
        costs=0,
        additional_facts=additional_info,
    )

    liability_insured_door = DoorNode(
        text="Wähle eine option",
    )

    liability_insured_event_good = EventNode(
        insurance="Haftplicht",
        cost=-5,
        text="""
Dein Freund erzählt dir was von einem coolen
neuen Job. Du bewirbst dich und wirst genommen.
        """,
        additional_info=additional_info,
    )

    liability_insured_event_bad = EventNode(
        insurance="Haftplicht",
        cost=0,
        text="""
Beim Spiel schießt du den Ball nicht ins Tor, 
sondern ins Fenster deines Nachbarn. Nachdem ihr die Klingel 
des Nachbarn gefunden habt, hoffst du, dass wenigstens der Ball 
ganz geblieben ist. Beim Rausgehen verliert er jedoch sein letztes 
bisschen Luft und alle Hoffnung ist dahin.
""",
        additional_info=additional_info,
    )

    liability_not_insured_door = DoorNode(
        text="Wähle eine Option",
    )

    liability_not_insured_event_bad1 = EventNode(
        insurance="Haftpflicht",
        costs=5,
        text="""
Der Ball zerstört das Fenster des Nachbarn ,
leider hast du keine Versicherung musst für den schaden aufkommen.(-5 Nautis)
        """,
        additional_info="""

""",
    )

    liability_not_insured_event_bad2 = EventNode(
        insurance="Haftpflicht",
        costs=8,
        text="""
Dein Ball fliegt ins Gesicht deines Freundes und bricht ihn die Nase.
Leider hast du keine Versicherung daher(-8 Nautis)
        """,
        additional_info="""

""",
    )

    liability_not_insured_event_good = EventNode(
        inurance="Haftpflicht",
        costs=-3,
        text="""
Ein Talentscout wird auf dich aufmerksam.(+3 Nautis)
        """,
        additional_info="""

""",
    )

    possibility_to_insure = ChapterNode(
        insurance="Haftpflicht",
        text="""

""",
        costs=0,
    )

    liability_not_insured_event_bad1.next_node = possibility_to_insure
    liability_not_insured_event_bad2.next_node = possibility_to_insure

    liability_insured_door.options = [
        liability_insured_event_good,
        liability_insured_event_bad,
    ]  # TODO: third option

    liability_not_insured_door.options = [
        liability_not_insured_event_bad1,
        liability_not_insured_event_bad2,
        liability_not_insured_event_good,
    ]

    shuffle(liability_insured_door.options)
    shuffle(liability_not_insured_door.options)

    liability_chapter.options = [liability_insured_door, liability_not_insured_door]

    return liability_chapter


def get_household_chapter() -> ChapterNode:

    """Household Chapter"""
    household_chapter = ChapterNode(
        insurance="Hausrats",
        text="""

""",
    )

    household_insured_door = DoorNode(
        text="Wähle eine Option.",
    )

    household_insured_event_bad = EventNode(
        insurance="Hausrats",
        costs=0,
        text="""

""",
        additional_info="""

""",
    )

    household_insured_event_good1 = EventNode(
        insurance="Hausrats",
        costs=0,
        text="""

""",
        additional_info="""

""",
    )

    household_insured_event_good2 = EventNode(
        insurance="Hausrats",
        costs=0,
        text="""

""",
        additional_info="""

""",
    )

    household_not_insured_door = DoorNode(
        text="Wähle eine Option.",
    )

    household_not_insured_event_bad1 = EventNode(
        insurance="Hausrats",
        costs=0,
        text="""

""",
        additional_info="""

""",
    )

    household_not_insured_event_bad2 = EventNode(
        insurance="Hausrats",
        costs=0,
        text="""

""",
        additional_info="""

""",
    )

    household_not_insured_event_good = EventNode(
        insurance="Hausrats",
        costs=0,
        text="""

""",
        additional_info=""" """,
    )

    possibility_to_insure = ChapterNode(
        insurance="Hausrats",
        text=""" 

""",
        costs=0,
    )

    household_not_insured_event_bad1.next_node = possibility_to_insure
    household_not_insured_event_bad2.next_node = possibility_to_insure

    household_insured_door.options = [
        household_insured_event_bad,
        household_insured_event_good1,
        household_insured_event_good2,
    ]

    household_not_insured_door.options = [
        household_not_insured_event_bad1,
        household_not_insured_event_bad2,
        household_not_insured_event_good,
    ]

    shuffle(household_insured_door.options)
    shuffle(household_not_insured_door.options)

    household_chapter.options = [household_insured_door, household_not_insured_door]

    return household_chapter


def get_vehicle_chapter() -> ChapterNode:

    """Vehicle Chapter"""
    vehicle_chapter = ChapterNode(
        insurance="KFZ",
        text="""

""",
        costs=0,
    )

    vehicle_insured_door = DoorNode(
        text="Wähle eine Option.",
    )

    vehicle_insured_event_bad = EventNode(
        insurance="KFZ",
        costs=0,
        text="""

""",
        additional_info="""

""",
    )

    vehicle_insured_event_good1 = EventNode(
        insurance="KFZ",
        costs=0,
        text="""

""",
        additional_info="""

""",
    )

    vehicle_insured_event_good2 = EventNode(
        insurance="KFZ",
        costs=0,
        text="""

""",
        additional_info="""

""",
    )

    vehicle_not_insured_door = DoorNode(
        text="Wähle eine Option.",
    )

    vehicle_not_insured_event_bad1 = EventNode(
        insurance="KFZ",
        costs=0,
        text="""

""",
        additional_info="""

""",
    )

    vehicle_not_insured_event_bad2 = EventNode(
        insurance="KFZ",
        costs=0,
        text="""

""",
        additional_info="""

""",
    )

    vehicle_not_insured_event_good = EventNode(
        insurance="KFZ",
        costs=0,
        text="""

""",
        additional_info="""

""",
    )

    possibility_to_insure = ChapterNode(
        insurance="KFZ",
        text="""

""",
        costs=0,
    )

    vehicle_not_insured_event_bad1.next_node = possibility_to_insure
    vehicle_not_insured_event_bad2.next_node = possibility_to_insure

    vehicle_insured_door.options = [
        vehicle_insured_event_bad,
        vehicle_insured_event_good1,
        vehicle_insured_event_good2,
    ]

    vehicle_not_insured_door.options = [
        vehicle_not_insured_event_bad1,
        vehicle_not_insured_event_bad2,
        vehicle_not_insured_event_good,
    ]

    shuffle(vehicle_insured_door.options)
    shuffle(vehicle_not_insured_door.options)

    vehicle_chapter.options = [vehicle_insured_door, vehicle_not_insured_door]

    return vehicle_chapter


def get_disability_chapter() -> ChapterNode:

    """Disability Chapter"""
    disability_chapter = ChapterNode(
        insurance="Berufsunfaehigkeit",
        text="""

""",
    )

    disability_insured_door = DoorNode(
        text="Wähle eine Option.",
    )

    disability_insured_event_bad = EventNode(
        insurance="Berufsunfaehigkeit",
        costs=0,
        text="""

""",
        additional_info="""

""",
    )

    disability_insured_event_good1 = EventNode(
        insurance="Berufsunfaehigkeit",
        costs=0,
        text="""
        
""",
        additional_info="""
        
""",
    )

    disability_insured_event_good2 = EventNode(
        insurance="Berufsunfaehigkeit",
        costs=0,
        text="""
        
""",
        additional_info="""
        
""",
    )

    disability_not_insured_door = DoorNode(
        text="Wähle eine Option.",
    )

    disability_not_insured_event_bad1 = EventNode(
        insurance="Berufsunfaehigkeit",
        costs=0,
        text="""
        
""",
        additional_info="""
        
""",
    )

    disability_not_insured_event_bad2 = EventNode(
        insurance="Berufsunfaehigkeit",
        costs=0,
        text="""
        
""",
        additional_info=""" """,
    )

    disability_not_insured_event_good = EventNode(
        insurance="Berufsunfaehigkeit",
        costs=0,
        text="""
        
""",
        additional_info="""
        
""",
    )

    disability_insured_door.options = [
        disability_insured_event_bad,
        disability_insured_event_good1,
        disability_insured_event_good2,
    ]

    disability_not_insured_door.options = [
        disability_not_insured_event_bad1,
        disability_not_insured_event_bad2,
        disability_not_insured_event_good,
    ]

    shuffle(disability_insured_door.options)
    shuffle(disability_not_insured_door.options)

    disability_chapter.options = [disability_insured_door, disability_not_insured_door]

    return disability_chapter


def create_chapter(
    insurance_name,
    chapter_text,
    costs_first_door,
    first_door_events_text,
    costs_second_door,
    second_door_events_text,
    additional_info,
):
    chapter = ChapterNode(
        insurance=insurance_name,
        text=chapter_text,
    )

    first_door = DoorNode(
        text="Wähle eine Option.",
    )

    for i in range(3):
        first_door_event = EventNode(
            insurance=insurance_name,
            costs=costs_first_door[i],
            text=first_door_events_text[i],
            additional_info=additional_info,
        )
        first_door.options.append(first_door_event)

    second_door = DoorNode(
        text="Wähle eine Option.",
    )

    for i in range(3):
        second_door_event = EventNode(
            insurance=insurance_name,
            costs=costs_second_door[i],
            text=second_door_events_text[i],
            additional_info=additional_info,
        )
        second_door.options.append(second_door_event)

    shuffle(first_door.options)
    shuffle(second_door.options)

    chapter.options = [first_door, second_door]

    return chapter


def start_story() -> Story:
    node = get_vacation_story_tree()
    story = Story(root_node=node)
    return story
