import os
import fitz  # PyMuPDF
from typing import List, Dict, Any

def calculate_invoice_totals(
    items: List[Dict[str, Any]],
    tax_rate_pct: float = 18.0,
    discount_amount: float = 0.0
) -> Dict[str, Any]:
    subtotal = sum(float(item["quantity"]) * float(item["unit_price"]) for item in items)
    taxable = max(0.0, subtotal - discount_amount)
    tax_amount = round(taxable * (tax_rate_pct / 100.0), 2)
    total_amount = round(taxable + tax_amount, 2)

    return {
        "subtotal": round(subtotal, 2),
        "discount_amount": round(discount_amount, 2),
        "tax_rate_pct": tax_rate_pct,
        "tax_amount": tax_amount,
        "total_amount": total_amount
    }

def generate_invoice_pdf(
    invoice_number: str,
    business_name: str,
    customer_name: str,
    customer_phone: str,
    issue_date: str,
    items: List[Dict[str, Any]],
    totals: Dict[str, Any],
    output_path: str
) -> str:
    """Generates a print-ready vector PDF invoice using PyMuPDF with guaranteed file closure."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = fitz.open()
    try:
        page = doc.new_page(width=595, height=842)

        # Header Banner
        page.draw_rect(fitz.Rect(40, 40, 555, 110), color=None, fill=(0.06, 0.09, 0.16))
        page.insert_text((60, 75), business_name, fontname="helv", fontsize=20, color=(1, 1, 1))
        page.insert_text((60, 95), "Official Tax Invoice & Receipt", fontname="helv", fontsize=10, color=(0.7, 0.75, 0.8))
        page.insert_text((420, 80), f"INVOICE: #{invoice_number}", fontname="helv", fontsize=12, color=(0.3, 0.7, 1))

        # Meta Section
        page.insert_text((40, 140), f"Billed To: {customer_name}", fontname="helv", fontsize=11, color=(0, 0, 0))
        page.insert_text((40, 155), f"Contact: {customer_phone}", fontname="helv", fontsize=10, color=(0.3, 0.3, 0.3))
        page.insert_text((420, 140), f"Date: {issue_date}", fontname="helv", fontsize=10, color=(0.3, 0.3, 0.3))
        page.insert_text((420, 155), "Status: PAID", fontname="helv", fontsize=10, color=(0.1, 0.7, 0.3))

        # Table Header
        page.draw_rect(fitz.Rect(40, 180, 555, 205), color=None, fill=(0.92, 0.94, 0.98))
        page.insert_text((50, 197), "Item Description", fontname="helv", fontsize=10, color=(0.1, 0.1, 0.1))
        page.insert_text((320, 197), "Qty", fontname="helv", fontsize=10, color=(0.1, 0.1, 0.1))
        page.insert_text((390, 197), "Unit Price", fontname="helv", fontsize=10, color=(0.1, 0.1, 0.1))
        page.insert_text((490, 197), "Total", fontname="helv", fontsize=10, color=(0.1, 0.1, 0.1))

        # Items
        y = 225
        for item in items:
            page.insert_text((50, y), str(item["description"]), fontname="helv", fontsize=9, color=(0.1, 0.1, 0.1))
            page.insert_text((325, y), str(item["quantity"]), fontname="helv", fontsize=9, color=(0.1, 0.1, 0.1))
            page.insert_text((390, y), f"INR {item['unit_price']:.2f}", fontname="helv", fontsize=9, color=(0.1, 0.1, 0.1))
            page.insert_text((490, y), f"INR {item['line_total']:.2f}", fontname="helv", fontsize=9, color=(0.1, 0.1, 0.1))
            page.draw_line(fitz.Point(40, y + 8), fitz.Point(555, y + 8), color=(0.85, 0.85, 0.85))
            y += 25

        # Totals Section
        y += 20
        page.insert_text((370, y), f"Subtotal: INR {totals['subtotal']:.2f}", fontname="helv", fontsize=10, color=(0.2, 0.2, 0.2))
        y += 18
        page.insert_text((370, y), f"Tax (GST {totals['tax_rate_pct']}%): INR {totals['tax_amount']:.2f}", fontname="helv", fontsize=10, color=(0.2, 0.2, 0.2))
        y += 22
        page.draw_rect(fitz.Rect(360, y - 14, 555, y + 14), color=None, fill=(0.06, 0.09, 0.16))
        page.insert_text((370, y + 4), f"TOTAL: INR {totals['total_amount']:.2f}", fontname="helv", fontsize=12, color=(1, 1, 1))

        # Footer
        page.insert_text((180, 800), "Generated with BizDesk - Thank you for your business!", fontname="helv", fontsize=9, color=(0.6, 0.6, 0.6))
        doc.save(output_path)
    finally:
        doc.close()

    return output_path
