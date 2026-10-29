"""भूमिका र अनुमति (role-based access).

हरेक अनुमति एउटा code हो (जस्तै "uc.approve")। कुन भूमिकालाई के अनुमति छ भन्ने:
  1. Admin ले "भूमिका र अनुमति" पेजमा बदलेको भए त्यही (RolePermission)
  2. नत्र तलको DEFAULT_ROLE_PERMS
थप, कुनै व्यक्तिलाई छुट्टै अनुमति दिन सकिन्छ (UserPermission) — जस्तै CAO ले
रुजु/स्वीकृतको अधिकार कुनै अधिकृतलाई प्रत्यायोजन गर्दा।

प्रयोग:  from accounts.permissions import has_perm
         if has_perm(request.user, "uc.approve"): ...
टेम्प्लेटमा: {% if 'uc.approve' in me.perms %}
"""

ROLES = [
    ("1", "प्रशासक (Admin)"),
    ("2", "प्रमुख प्रशासकीय अधिकृत"),
    ("3", "योजना अधिकृत"),
    ("4", "इन्जिनियर"),
    ("5", "वडा कर्मचारी"),
    ("6", "वडा सचिव"),
    ("7", "वडा इन्जिनियर"),
    ("8", "पालिका इन्जिनियर"),
    ("9", "वडा अध्यक्ष"),
]
ROLE_LABEL = dict(ROLES)

# (code, group, label, help)
PERMISSIONS = [
    ("project.manage", "योजना", "योजना दर्ता / सम्पादन", "नयाँ योजना थप्ने र सच्याउने"),

    ("uc.committee", "उपभोक्ता समिति", "समिति गठन / सम्पादन", "पदाधिकारी, सदस्य र तिनका कागजात राख्ने (वडा तहका कर्मचारीले आफ्नै वडाको मात्र)"),
    ("uc.member_docs", "उपभोक्ता समिति", "सदस्यका कागजात हेर्ने", "नागरिकता, NID र फोटो हेर्ने"),
    ("uc.estimate", "उपभोक्ता समिति", "लागत अनुमान थप्ने", ""),
    ("uc.estimate_edit", "उपभोक्ता समिति", "लागत अनुमान सच्याउने", "स्वीकृत हुनुअघि मात्र"),

    ("uc.sifaris_portal", "वडा सिफारिस", "पोर्टलबाट सिफारिस गर्ने", "वडा सचिवले आफ्नो वडाको"),
    ("uc.sifaris_upload", "वडा सिफारिस", "कागजी सिफारिस अपलोड गर्ने", "वडाबाट कागजमा आएको सिफारिस स्क्यान गरी राख्ने"),

    ("uc.approve", "रुजु / स्वीकृत", "रुजु / स्वीकृत गर्ने (सबै योजना)", "पालिका केन्द्रित र वडा प्रत्यायोजित दुवै"),
    ("uc.approve_ward", "रुजु / स्वीकृत", "आफ्नो वडाको योजना स्वीकृत गर्ने", "वडा प्रत्यायोजित तरिकाका, आफ्नै वडाका योजना मात्र"),
    ("uc.delegate", "रुजु / स्वीकृत", "स्वीकृत अधिकार प्रत्यायोजन गर्ने", "अरू अधिकृतलाई रुजु / स्वीकृतको अधिकार दिने/हटाउने"),

    ("uc.public_audit", "सम्झौता र भुक्तानी", "सार्वजनिक परीक्षण / अनुगमन विवरण राख्ने", "मुचुल्का, उपस्थिति, फोटो र अनुगमन समितिको प्रतिवेदन"),
    ("uc.agreement_print", "सम्झौता र भुक्तानी", "सम्झौता, टिप्पणी, बैंक पत्र, कार्यादेश छाप्ने", ""),
    ("uc.valuation", "सम्झौता र भुक्तानी", "अन्तिम मूल्याङ्कन गर्ने", ""),
    ("uc.payment_print", "सम्झौता र भुक्तानी", "अन्तिम टिप्पणी / हस्तान्तरण छाप्ने", ""),

    ("uc.progress_photo", "काम प्रगति", "प्रगति फोटो अपलोड", ""),
    ("uc.inspection", "काम प्रगति", "निरीक्षण टिप्पणी", ""),

    ("bid.view", "बोलपत्र ठेक्का", "ठेक्का कार्यप्रवाह हेर्ने", "बोलपत्र, सम्झौता, जमानत र भुक्तानीको स्थिति"),
    ("bid.manage", "बोलपत्र ठेक्का", "ठेक्का विवरण भर्ने", "आह्वान, मूल्याङ्कन, PG माग, सम्झौता, पेश्की, रनिङ र अन्तिम बिल"),
    ("bid.approve", "बोलपत्र ठेक्का", "बोलपत्र रुजु / स्वीकृत गर्ने", "मूल्याङ्कन र आशयको सूचनापछि"),
    ("bid.print", "बोलपत्र ठेक्का", "ठेक्काका कागजात छाप्ने", "आशयको सूचना, टिप्पणी, सम्झौता, कार्यादेश, भुक्तानी टिप्पणी"),

    ("quot.view", "दरभाउपत्र खरिद", "दरभाउपत्र कार्यप्रवाह हेर्ने", "आह्वान, तुलना, सम्झौता र भुक्तानीको स्थिति"),
    ("quot.manage", "दरभाउपत्र खरिद", "दरभाउपत्र विवरण भर्ने", "सूचीकृत फर्म, आह्वान, प्राप्त दर, सम्झौता र अन्तिम बिल"),
    ("quot.approve", "दरभाउपत्र खरिद", "दरभाउपत्र रुजु / स्वीकृत गर्ने", "न्यूनतम दर स्वीकृत"),
    ("quot.print", "दरभाउपत्र खरिद", "दरभाउपत्रका कागजात छाप्ने", "आह्वान पत्र, टिप्पणी, सम्झौता, कार्यादेश, भुक्तानी टिप्पणी"),

    ("retention.recommend", "धरौटी फिर्ता", "धरौटी फिर्ता सिफारिस अपलोड गर्ने", "इन्जिनियर वा वडाको सिफारिस पत्र (स्क्यान) राख्ने"),
    ("retention.manage", "धरौटी फिर्ता", "धरौटी फिर्ता टिप्पणी र फिर्ता दर्ता", "सिफारिसपछि टिप्पणी छाप्ने, फिर्ता भएको दर्ता गर्ने"),

    ("budget.view", "बजेट नियन्त्रण", "बजेट स्थिति हेर्ने", "शीर्षक/योजनाअनुसार विनियोजित, प्रतिबद्धता, खर्च र बाँकी"),
    ("budget.manage", "बजेट नियन्त्रण", "बजेट शीर्षक र रकमान्तर", "बजेट शीर्षक थप्ने/बदल्ने; योजनाको बजेट थप, कटौती, रकमान्तर दर्ता गर्ने"),

    ("letters.edit", "पत्र", "पत्र सम्पादन (एउटा पत्र मात्र)", "छाप्नुअघि त्यही योजनाको पत्रको पाठ बदल्ने"),
    ("letters.templates", "पत्र", "पत्रको ढाँचा (सबै योजनामा)", "पालिकाको ढाँचा — placeholder सहित, सबै पत्रमा लागू"),
    ("report.uc", "प्रतिवेदन", "खरिद तथा भुक्तानी प्रतिवेदन", "उपभोक्ता समिति, बोलपत्र, दरभाउपत्र — विनियोजित, भुक्तानी, कर कट्टी (एकीकृत वा छुट्टै)"),
    ("report.outputs", "प्रतिवेदन", "भौतिक उपलब्धि प्रतिवेदन", "कति कि.मि. बाटो, कति भवन … (सबै वडा, आ.व. अनुसार)"),
    ("settings.staff", "सेटिङ", "कर्मचारी व्यवस्थापन", ""),
    ("settings.tax", "सेटिङ", "कर शीर्षक", "अन्तिम भुक्तानीमा कट्टी हुने करका शीर्षक थप्ने/बदल्ने"),
    ("settings.office", "सेटिङ", "कार्यालय सेटिङ र पत्र शीर्ष", "लोगो, नारा, वेबसाइट, इमेल र पत्र शीर्ष मिलाउने"),
    ("settings.sectors", "सेटिङ", "क्षेत्र / उपक्षेत्र", "योजनाको क्षेत्र र उपक्षेत्र थप्ने/बदल्ने"),
    ("settings.outputs", "सेटिङ", "कामको प्रकार र उपलब्धि सूचक", "सडक, भवन … र तिनका सूचक (कि.मि., वटा) थप्ने/बदल्ने"),
    ("settings.roles", "सेटिङ", "भूमिका र अनुमति मिलाउने", "Admin को यो अनुमति हटाउन मिल्दैन"),
]
PERM_LABEL = {c: l for c, _g, l, _h in PERMISSIONS}
PERM_CODES = set(PERM_LABEL)

# Admin बाट कहिल्यै नहट्ने (आफैँलाई बाहिर थुन्न नमिल्ने)
LOCKED = {("1", "settings.roles")}

ALL = {c for c, *_ in PERMISSIONS}
DEFAULT_ROLE_PERMS = {
    "1": ALL - {"uc.approve_ward"},
    "2": {"uc.approve", "uc.delegate", "uc.member_docs", "uc.agreement_print", "uc.payment_print", "letters.edit",
          "report.outputs", "report.uc", "bid.view", "bid.approve", "bid.print",
          "quot.view", "quot.approve", "quot.print", "retention.manage", "budget.view"},
    "3": {"uc.public_audit", "project.manage", "uc.committee", "uc.member_docs", "uc.estimate", "uc.sifaris_upload",
          "uc.agreement_print", "uc.valuation", "uc.payment_print", "letters.edit", "report.outputs", "report.uc", "settings.outputs", "settings.sectors",
          "bid.view", "bid.manage", "bid.print", "quot.view", "quot.manage", "quot.print",
          "retention.recommend", "retention.manage", "budget.view", "budget.manage"},
    "4": {"uc.estimate", "bid.view", "quot.view", "retention.recommend"},
    "5": {"uc.sifaris_upload"},
    "6": {"uc.public_audit", "uc.committee", "uc.member_docs", "uc.sifaris_portal", "letters.edit", "retention.recommend"},
    "7": {"uc.public_audit", "uc.estimate", "uc.progress_photo", "retention.recommend"},
    "8": {"uc.public_audit", "uc.estimate", "uc.estimate_edit", "uc.inspection", "report.outputs", "report.uc",
          "bid.view", "quot.view", "retention.recommend", "budget.view"},
    "9": {"uc.approve_ward", "uc.member_docs"},
}

# व्यक्तिगत रूपमा दिन मिल्ने अनुमति (प्रत्यायोजन) र कसलाई दिन मिल्ने
GRANTABLE = {
    "uc.approve": {"1", "3", "4", "8"},   # CAO ले प्रत्यायोजन गर्ने अधिकृत
}


def role_perms(role):
    """एउटा भूमिकाका प्रभावी अनुमति (Admin ले बदलेको + default)."""
    from .models import RolePermission

    perms = set(DEFAULT_ROLE_PERMS.get(str(role), set()))
    for perm, allowed in RolePermission.objects.filter(role=str(role)).values_list("perm", "allowed"):
        if (str(role), perm) in LOCKED:
            continue
        (perms.add if allowed else perms.discard)(perm)
    perms |= {p for r, p in LOCKED if r == str(role)}
    return perms & PERM_CODES


def user_perms(user):
    """प्रयोगकर्ताका सबै अनुमति (भूमिका + व्यक्तिगत), एउटा request भित्र cache।"""
    if not getattr(user, "is_authenticated", False):
        return frozenset()
    cached = getattr(user, "_pms_perms", None)
    if cached is not None:
        return cached
    from .models import UserPermission

    perms = role_perms(user.user_type)
    perms |= set(UserPermission.objects.filter(user=user).values_list("perm", flat=True))
    user._pms_perms = frozenset(perms)
    return user._pms_perms


def has_perm(user, code):
    return code in user_perms(user)


def clear_cache(user):
    if hasattr(user, "_pms_perms"):
        del user._pms_perms
