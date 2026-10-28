"""उपभोक्ता समिति प्रतिवेदन — योजनाअनुसार रकम (विनियोजित, लागत अनुमान, भुक्तानी, कर) र एकीकृत सारांश.

भुक्तानी (कुल):  अन्तिम मूल्याङ्कन भए FinalPayment.office_contribution (किस्ता समेत),
                 नभए दिइसकेका किस्ताको जम्मा।
कर कट्टी:        अन्तिम भुक्तानीको कर + हरेक किस्ताको कर (शीर्षकअनुसार)।
खुद भुक्तानी:    कुल भुक्तानी − कर।
सम्पन्न:          workflow का सबै चरण पूरा (हस्तान्तरणसम्म)।
"""
from collections import OrderedDict
from decimal import Decimal

ZERO = Decimal("0")
STATUS = OrderedDict([
    ("completed", "सम्पन्न"),
    ("paid", "भुक्तानी भएको (हस्तान्तरण बाँकी)"),
    ("running", "चालु"),
    ("not_started", "समिति गठन बाँकी"),
])


def D(v):
    return Decimal(str(v or 0))


def as_dict(v):
    """tax_deduction — पुराना अभिलेखमा text भए पनि dict."""
    if isinstance(v, dict):
        return v
    if isinstance(v, str) and v.strip():
        import json
        try:
            parsed = json.loads(v)
            return parsed if isinstance(parsed, dict) else {}
        except ValueError:
            return {}
    return {}


def _status(project, summary):
    if summary["completed"]:
        return "completed"
    if getattr(project, "final_payment", None) is not None:
        return "paid"
    if getattr(project, "user_committee", None) is None:
        return "not_started"
    return "running"


def project_rows(qs, status=""):
    """हरेक योजनाको रकम र स्थिति। status दिए त्यही स्थितिका मात्र।"""
    from .workflow import project_workflow

    rows = []
    for p in qs:
        _steps, summary = project_workflow(p)
        st = _status(p, summary)
        if status and st != status:
            continue
        uc = getattr(p, "user_committee", None)
        est = getattr(p, "cost_estimate", None)
        fp = getattr(p, "final_payment", None)
        insts = list(p.installments.all())
        inst_amount = sum((i.amount for i in insts), ZERO)
        taxes = {}
        for src in ([fp.tax_deduction] if fp else []) + [i.tax_deduction for i in insts]:
            for code, v in as_dict(src).items():
                taxes[code] = taxes.get(code, ZERO) + D(v)
        gross = D(fp.office_contribution) if fp else inst_amount
        tax = sum(taxes.values(), ZERO)
        allocated = D(p.budget)
        rows.append({
            "p": p, "uc": uc, "status": st, "status_label": STATUS[st],
            "allocated": allocated,
            "estimate": D(est.total_cost) if est else None,
            "office_share": (D(est.budget) - D(est.contingency_amount)) if est else None,
            "contingency": D(est.contingency_amount) if est else ZERO,
            "user_share": D(est.user_contribution) if est else ZERO,
            "valuation": D(fp.final_evaluation) if fp else None,
            "installments": inst_amount, "inst_count": len(insts),
            "gross": gross, "tax": tax, "taxes": taxes, "net": gross - tax,
            "remaining": allocated - gross,
            "work_category": p.work_category.name if p.work_category_id else "",
        })
    return rows


def totals(rows):
    keys = ("allocated", "contingency", "user_share", "installments", "gross", "tax", "net", "remaining")
    t = {k: sum((r[k] for r in rows), ZERO) for k in keys}
    t["estimate"] = sum((r["estimate"] for r in rows if r["estimate"] is not None), ZERO)
    t["office_share"] = sum((r["office_share"] for r in rows if r["office_share"] is not None), ZERO)
    t["valuation"] = sum((r["valuation"] for r in rows if r["valuation"] is not None), ZERO)
    t["count"] = len(rows)
    t["by_status"] = OrderedDict((k, sum(1 for r in rows if r["status"] == k)) for k in STATUS)
    t["paid_pct"] = round(t["gross"] * 100 / t["allocated"], 1) if t["allocated"] else 0
    return t


def by_ward(rows, wards):
    out = []
    for w in wards:
        rs = [r for r in rows if r["p"].ward_id == w.id]
        if rs:
            out.append({"ward": w, **totals(rs)})
    other = [r for r in rows if r["p"].ward_id not in {w.id for w in wards}]
    if other:
        out.append({"ward": None, **totals(other)})
    return out


def by_tax_head(rows, wards):
    """[{"code", "name", "total", "count", "ward_values": [...], "projects": [(row, amount)]}] — शीर्षकअनुसार।"""
    from .tax import tax_labels

    labels = tax_labels()
    order = {}
    try:
        from .models import TaxHead
        order = {h.code: (h.sort, h.id) for h in TaxHead.objects.all()}
    except Exception:
        pass
    heads = {}
    for r in rows:
        for code, v in r["taxes"].items():
            h = heads.setdefault(code, {"code": code, "name": labels.get(code, code), "total": ZERO,
                                        "projects": [], "by_ward": {}})
            h["total"] += v
            h["projects"].append((r, v))
            h["by_ward"][r["p"].ward_id] = h["by_ward"].get(r["p"].ward_id, ZERO) + v
    out = sorted(heads.values(), key=lambda h: order.get(h["code"], (999, h["name"])))
    for h in out:
        h["count"] = len(h["projects"])
        h["ward_values"] = [h["by_ward"].get(w.id) for w in wards]
    return out
