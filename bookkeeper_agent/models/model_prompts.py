RECEIPT_EXTRACTION_SYSTEM_PROMPT = (
	"You are an assistant that extracts structured receipt data as JSON with keys: "
	"date (YYYY-MM-DD), vendor, amount (number), category, currency (optional)."
)

RECEIPT_EXTRACTION_USER_PROMPT = (
	"Extract receipt fields from the following text. If you are unsure, return empty values.\n\n{receipt_text}"
) 