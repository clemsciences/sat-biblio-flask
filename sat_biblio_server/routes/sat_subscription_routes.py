"""
Route to handle SAT subscription form submission: generates XLSX and PDF attachments and sends emails.
"""
import os
from io import BytesIO
from datetime import datetime

from flask import current_app, request
from flask_mail import Message

from sat_biblio_server import sat_biblio
from sat_biblio_server.utils import json_result
from sat_biblio_server.managers.mail_manager import send_email

try:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment
    from openpyxl.utils import get_column_letter
except Exception:  # pragma: no cover
    Workbook = None
    Alignment = None
    get_column_letter = None

try:
    from fpdf import FPDF
except Exception:  # pragma: no cover
    FPDF = None

FONTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "fonts")

SAT_EMAIL = "admin@societearcheotouraine.fr"


def _compute_total(membership_type: str, receive_bulletin_by_post: bool) -> int:
    base = 0
    if membership_type == "student":
        base = 10
    elif membership_type == "single":
        base = 46
    elif membership_type == "couple":
        base = 62
    # if no membership selected we consider total 0
    if receive_bulletin_by_post:
        base += 13
    return base


PAYMENT_INSTRUCTIONS = {
    "cheque": (
        "Chèque",
        "Merci d'établir un chèque à l'ordre de la Société archéologique de Touraine.\n"
        "Adresse d'envoi: 37 avenue André Malraux.\n"
        "Vous pouvez aussi déposer le chèque à la BHT."
    ),
    "virement": (
        "Virement bancaire",
        "Merci d'effectuer un virement bancaire au compte de la SAT.\n"
        "IBAN: FR76 3000 0000 0000 0000 0000 000\nBIC: XXXXXX\n"
        "Indiquez en référence: Adhésion SAT - {last_name} {first_name}."
    ),
    "carte": (
        "Carte bancaire ou espèces",
        "Paiement par carte bancaire ou en espèces à la BHT (mardi 18h-21h ; mercredi et samedi 10h-13h)\n"
        "ou lors des séances mensuelles."
    )
}


def _build_payment_instruction(method: str, first_name: str, last_name: str) -> str:
    title, text = PAYMENT_INSTRUCTIONS.get(method, ("", ""))
    return f"Mode de règlement choisi: {title}\n\n{text.format(first_name=first_name, last_name=last_name)}"


def _build_xlsx(payload: dict) -> bytes:
    if Workbook is None:
        # fallback: simple CSV-like bytes
        headers = [
            "Prénom", "Nom", "Adresse", "Téléphone fixe", "Téléphone mobile", "Courriel",
            "Profession", "Année de naissance",
            "Prénom (2)", "Nom (2)", "Profession (2)", "Année de naissance (2)",
            "Type d'adhésion", "Bulletin par la poste", "Montant total", "Règlement",
            "Recevoir infos par courrier", "Refus publication"
        ]
        row = [
            payload.get("firstName", ""),
            payload.get("lastName", ""),
            payload.get("address", ""),
            payload.get("phoneLandline", ""),
            payload.get("phoneMobile", ""),
            payload.get("email", ""),
            payload.get("profession", ""),
            payload.get("birthYear", ""),
            payload.get("secondFirstName", ""),
            payload.get("secondLastName", ""),
            payload.get("secondProfession", ""),
            payload.get("secondBirthYear", ""),
            payload.get("membershipType", ""),
            "oui" if payload.get("receiveBulletinByPost") else "non",
            payload.get("totalAmount", 0),
            payload.get("paymentMethod", ""),
            "oui" if payload.get("mustReceiveInfoByMail") else "non",
            "oui" if payload.get("refusePublishInfo") else "non",
        ]
        content = ";".join(map(str, headers)) + "\n" + ";".join(map(lambda x: str(x).replace("\n", " "), row))
        return content.encode("utf-8")

    wb = Workbook()
    ws = wb.active
    ws.title = "Adhésion SAT"
    ws.append([
        "Prénom", "Nom", "Adresse", "Téléphone fixe", "Téléphone mobile", "Courriel",
        "Profession", "Année de naissance",
        "Prénom (2)", "Nom (2)", "Profession (2)", "Année de naissance (2)",
        "Type d'adhésion", "Bulletin par la poste", "Montant total", "Règlement",
        "Recevoir infos par courrier", "Refus publication", "Date"
    ])
    ws.append([
        payload.get("firstName", ""),
        payload.get("lastName", ""),
        payload.get("address", ""),
        payload.get("phoneLandline", ""),
        payload.get("phoneMobile", ""),
        payload.get("email", ""),
        payload.get("profession", ""),
        payload.get("birthYear", ""),
        payload.get("secondFirstName", ""),
        payload.get("secondLastName", ""),
        payload.get("secondProfession", ""),
        payload.get("secondBirthYear", ""),
        payload.get("membershipType", ""),
        "oui" if payload.get("receiveBulletinByPost") else "non",
        payload.get("totalAmount", 0),
        payload.get("paymentMethod", ""),
        "oui" if payload.get("mustReceiveInfoByMail") else "non",
        "oui" if payload.get("refusePublishInfo") else "non",
        datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    ])

    # Center content and wrap text, then auto-size columns and rows
    if Alignment is not None:
        # 1) Set alignment (center + wrap)
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            for cell in row:
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        # 2) Compute and apply column widths based on content length (max per column)
        if get_column_letter is not None:
            max_lengths = {}
            for col_idx in range(1, ws.max_column + 1):
                max_lengths[col_idx] = 0
                for row_idx in range(1, ws.max_row + 1):
                    value = ws.cell(row=row_idx, column=col_idx).value
                    if value is None:
                        continue
                    # handle multi-line: take the longest visual line
                    lines = str(value).splitlines() or [""]
                    longest = max(len(line) for line in lines)
                    if longest > max_lengths[col_idx]:
                        max_lengths[col_idx] = longest
            for col_idx, length in max_lengths.items():
                # Approximate: each character ~ 1 unit, add padding
                width = min(max(length + 2, 10), 60)
                ws.column_dimensions[get_column_letter(col_idx)].width = width

        # 3) Adjust row heights based on number of lines in cells
        base_height = 15  # approx default row height in points
        for row_idx in range(1, ws.max_row + 1):
            max_lines = 1
            for col_idx in range(1, ws.max_column + 1):
                value = ws.cell(row=row_idx, column=col_idx).value
                if value is None:
                    continue
                lines = str(value).splitlines() or [""]
                if len(lines) > max_lines:
                    max_lines = len(lines)
            # cap the row height to avoid excessively large rows
            ws.row_dimensions[row_idx].height = min(base_height * max_lines, 90)

    bio = BytesIO()
    wb.save(bio)
    return bio.getvalue()


MEMBERSHIP_LABELS = {
    "student": "Étudiant (10 €)",
    "single": "Inscription pour une personne (46 €)",
    "couple": "Inscription pour un couple (62 €)",
}


def _build_pdf(payload: dict):
    """
    Build a one-page PDF summary of the subscription form.
    Returns None if the PDF cannot be generated, so that the subscription is still sent.
    """
    if FPDF is None:
        return None
    try:
        pdf = FPDF(format="A4")
        pdf.set_margins(20, 20, 20)
        pdf.set_title("Demande d'adhésion à la SAT")
        pdf.add_page()

        regular = os.path.join(FONTS_DIR, "DejaVuSans.ttf")
        bold = os.path.join(FONTS_DIR, "DejaVuSans-Bold.ttf")
        unicode_font = os.path.exists(regular) and os.path.exists(bold)
        if unicode_font:
            pdf.add_font("DejaVu", "", regular)
            pdf.add_font("DejaVu", "B", bold)
            family = "DejaVu"
        else:
            # core fonts only know latin-1
            family = "Helvetica"

        def clean(value) -> str:
            text = "" if value is None else str(value).strip()
            if not unicode_font:
                text = text.replace("€", "EUR").replace("’", "'").replace("—", "-")
                text = text.encode("latin-1", "replace").decode("latin-1")
            return text

        def section(title: str):
            pdf.ln(4)
            pdf.set_font(family, "B", 12)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(0, 8, clean(title), fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)

        def field(label: str, value):
            pdf.set_font(family, "B", 10)
            pdf.cell(62, 6, clean(label))
            pdf.set_font(family, "", 10)
            pdf.multi_cell(0, 6, clean(value) or "-", new_x="LMARGIN", new_y="NEXT")

        def yes_no(value) -> str:
            return "oui" if value else "non"

        pdf.set_font(family, "B", 16)
        pdf.cell(0, 10, clean("Société Archéologique de Touraine"), align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(family, "", 13)
        pdf.cell(0, 8, clean("Demande d'adhésion"), align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(family, "", 9)
        pdf.cell(0, 6, clean(f"Demande du {datetime.now().strftime('%d/%m/%Y à %H:%M')}"), align="C",
                 new_x="LMARGIN", new_y="NEXT")

        section("Première personne")
        field("Prénom", payload.get("firstName"))
        field("Nom", payload.get("lastName"))
        field("Profession", payload.get("profession"))
        field("Année de naissance", payload.get("birthYear"))

        if payload.get("membershipType") == "couple":
            section("Deuxième personne")
            field("Prénom", payload.get("secondFirstName"))
            field("Nom", payload.get("secondLastName"))
            field("Profession", payload.get("secondProfession"))
            field("Année de naissance", payload.get("secondBirthYear"))

        section("Coordonnées")
        field("Adresse", payload.get("address"))
        field("Téléphone fixe", payload.get("phoneLandline"))
        field("Téléphone mobile", payload.get("phoneMobile"))
        field("Courriel", payload.get("email"))

        section("Adhésion")
        membership = payload.get("membershipType")
        field("Type d'adhésion", MEMBERSHIP_LABELS.get(membership, membership))
        field("Bulletin par la poste (+13 €)", yes_no(payload.get("receiveBulletinByPost")))
        field("Informations par courrier", yes_no(payload.get("mustReceiveInfoByMail")))
        field("Refus de publication", yes_no(payload.get("refusePublishInfo")))
        field("Montant total", f"{payload.get('totalAmount', 0)} €")
        pdf.set_font(family, "", 8)
        pdf.cell(0, 5, clean("Tarifs valables du 01/01/2025 au 31/12/2025."), new_x="LMARGIN", new_y="NEXT")

        section("Règlement")
        method = payload.get("paymentMethod")
        title, text = PAYMENT_INSTRUCTIONS.get(method, (method or "", ""))
        field("Mode de règlement", title)
        if text:
            pdf.ln(1)
            pdf.set_font(family, "", 10)
            pdf.multi_cell(0, 6, clean(text.format(first_name=payload.get("firstName", ""),
                                                   last_name=payload.get("lastName", ""))),
                           new_x="LMARGIN", new_y="NEXT")

        return bytes(pdf.output())
    except Exception:
        current_app.logger.exception("Impossible de générer le PDF d'adhésion")
        return None


def _compose_email_subject(payload: dict) -> str:
    first_name = payload.get("firstName", "")
    last_name = payload.get("lastName", "")
    membership = payload.get("membershipType", "?")
    return f"Nouvelle adhésion SAT - {last_name} {first_name} ({membership})"


def _compose_email_body(payload: dict, to_member: bool = False, with_pdf: bool = False) -> str:
    first_name = payload.get("firstName", "")
    last_name = payload.get("lastName", "")
    amount = payload.get("totalAmount", 0)
    method = payload.get("paymentMethod", "")
    instr = _build_payment_instruction(method, first_name, last_name)

    intro = (
        "Bonjour,\n\n"
        "Nous avons bien reçu votre demande d'adhésion à la Société Archéologique de Touraine.\n"
        if to_member else
        "Bonjour,\n\nUne nouvelle demande d'adhésion a été soumise.\n"
    )

    txt = (
        f"Adhérent: {first_name} {last_name}\n"
        "Tarifs valables du 01/01/2025 au 31/12/2025.\n"
        f"Montant à régler: {amount} €\n"
        f"{instr}\n\n"
    )
    if to_member:
        if with_pdf:
            txt += "Un récapitulatif de votre demande est joint à ce message au format PDF.\n\n"
    elif with_pdf:
        txt += "Les informations fournies sont jointes à ce message aux formats .xlsx et PDF.\n\n"
    else:
        txt += "Les informations fournies sont jointes à ce message sous forme de fichier .xlsx.\n\n"
    txt += "Ceci est un message automatique."
    return intro + txt


@sat_biblio.route("/send-sat", methods=["POST"])  # path required in issue description
@sat_biblio.route("/send-sat/", methods=["POST"])  # tolerate trailing slash
def send_sat_subscription():
    data = request.get_json() or {}

    # Basic required fields
    first_name = data.get("firstName", "").strip()
    last_name = data.get("lastName", "").strip()
    address = data.get("address", "").strip()
    membership_type = data.get("membershipType")
    receive_bulletin = bool(data.get("receiveBulletinByPost", False))
    payment_method = data.get("paymentMethod")

    if not first_name or not last_name or not address or not membership_type or not payment_method:
        return json_result(False, message="Champs manquants"), 400

    # compute total if not provided
    total = data.get("totalAmount")
    if total is None:
        total = _compute_total(membership_type, receive_bulletin)
        data["totalAmount"] = total

    # Build attachments
    xlsx_bytes = _build_xlsx(data)
    pdf_bytes = _build_pdf(data)
    with_pdf = pdf_bytes is not None

    # Compose and send to SAT
    subject = _compose_email_subject(data)
    msg_admin = Message(subject=subject)
    msg_admin.body = _compose_email_body(data, to_member=False, with_pdf=with_pdf)
    msg_admin.add_recipient(SAT_EMAIL)
    basename = f"adhesion_sat_{last_name}_{first_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    filename = f"{basename}.xlsx"
    msg_admin.attach(filename, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", xlsx_bytes)
    if with_pdf:
        msg_admin.attach(f"{basename}.pdf", "application/pdf", pdf_bytes)
    ok1 = send_email(msg_admin, SAT_EMAIL)

    # Send to member if email provided
    ok2 = True
    member_email = (data.get("email") or "").strip()
    if member_email:
        msg_member = Message(subject="Votre demande d'adhésion à la SAT")
        msg_member.body = _compose_email_body(data, to_member=True, with_pdf=with_pdf)
        msg_member.add_recipient(member_email)
        # msg_member.attach(filename, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", xlsx_bytes)
        if with_pdf:
            msg_member.attach(f"{basename}.pdf", "application/pdf", pdf_bytes)
        ok2 = send_email(msg_member, member_email)

    if ok1 and ok2:
        return json_result(True, message="Demande d'adhésion envoyée."), 200
    else:
        return json_result(False, message="Echec de l'envoi d'email."), 500
