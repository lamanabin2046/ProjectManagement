from django.db import connection

NEPALI_DIGITS = str.maketrans("0123456789", "०१२३४५६७८९")

ROLE_LABELS = {
    "1": "प्रशासक",
    "2": "प्रमुख प्रशासकीय अधिकृत",
    "3": "योजना अधिकृत",
    "4": "इन्जिनियर",
    "5": "वडा कर्मचारी",
    "6": "वडा सचिव",
    "7": "वडा इन्जिनियर",
    "8": "पालिका इन्जिनियर",
    "9": "वडा अध्यक्ष",
}
ROLE_PROFILE = {
    "1": "admin", "2": "cao", "3": "planningofficer", "4": "engineer", "5": "wadastaff",
    "6": "wardsachib", "7": "wardengineer", "8": "palikaengineer", "9": "wardchairperson",
}
ROLE_HOME = {
    "1": "admin_home", "2": "usercommittee_workflow", "3": "planning_home", "4": "engineer_home",
    "5": "usercommittee_workflow", "6": "ward_sachib_home", "7": "ward_engineer_home",
    "8": "palika_engineer_home", "9": "usercommittee_workflow",
}


def palika(request):
    """Expose the current palika to every template as {{ palika }}.

    On the SaaS manager (public schema) this is None.
    """
    tenant = getattr(request, "tenant", None) or getattr(connection, "tenant", None)
    if tenant is None or getattr(tenant, "schema_name", "public") == "public":
        return {"palika": None}
    return {"palika": tenant}


def _initials(name):
    parts = [p for p in (name or "").replace(".", " ").split() if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def me(request):
    """The signed-in person as shown in the header and the sidebar user card."""
    user = getattr(request, "user", None)
    ctx = {"today_bs": ""}
    try:
        from datetime import date

        from nepali.date_converter import converter

        d = date.today()
        y, m, dd = converter.english_to_nepali(d.year, d.month, d.day)
        ctx["today_bs"] = f"{y}-{m:02d}-{dd:02d}".translate(NEPALI_DIGITS)
    except Exception:
        pass
    if not user or not user.is_authenticated:
        return ctx
    t = str(getattr(user, "user_type", ""))
    profile = None
    attr = ROLE_PROFILE.get(t)
    if attr:
        try:
            profile = getattr(user, attr)
        except Exception:
            profile = None
    name = getattr(profile, "name", "") or user.get_full_name() or user.mobile
    role = ROLE_LABELS.get(t, "")
    ward = getattr(getattr(profile, "ward", None), "name", None)
    if ward:
        role = f"{role}, वडा नं. {ward}"
    perms = frozenset()
    try:
        from accounts.permissions import user_perms

        perms = user_perms(user)
    except Exception:
        pass
    ctx["me"] = {
        "perms": perms,
        "name": name,
        "initials": _initials(name),
        "role": role,
        "mobile": user.mobile,
        "home": ROLE_HOME.get(t, "usercommittee_workflow"),
    }
    return ctx
