# ============================================================
# config.py — Keywords and their exact auto-replies
# ============================================================
# HOW TO ADD MORE KEYWORDS:
#   - The KEY is what the user must send (exact word, case-insensitive)
#   - The VALUE is what your account will reply with
#   - Add as many as you want following the same pattern
# ============================================================

KEYWORD_REPLIES = {
    "Ads": (
        "Scale your business to 7 figures monthly with TikTok Ads.\n\n"
        "Click the link below to see how I've helped others achieve this "
        "and how I can help you.\n\n"
        "The link is available for a limited time. https://bit.ly/3MDhV0N"
    ),
    "Hello":(
        "Hi"
    ),
    "Hi":(
        "Hello"
    ),
    "Good morning":(
        "Good morning"
    ),
    "Good afternoon":(
        "Good afternoon"
    ),
    "Good evening":(
        "Good evening"
    ),
    "Good night":(
        "Good night"
    ),
    "How are you":(
        "I'm good, thank you"
    ),
    "How are you doing":(
        "I'm good, thank you"
    ),
    "How are you doing today":(
        "I'm good, thank you"
    ),
    "How are you doing today":(
        "I'm good, thank you"
    ),
    "Offer":(
        "Congratulations on showing interest for the DFY Tiktok Ads Offer \n\n"
        "Kindly transfer the sum of 50k to this account below \n\n"
        "Account Name: Tikmarketinghub \n\n"
        "Account Number: 3003247241 \n\n"
        "Bank Name: Kuda MFB \n\n"
        "And send your payment receipts afterwards."
    ),

    # ---- Add more keywords below this line ----
    # "Price": "Here is our pricing list: ...",
    # "Contact": "You can reach us at ...",
}


# ============================================================
# Follow-up message sent after 1 hour of no reply from user
# {first_name} is automatically replaced with the user's name
# ============================================================
FOLLOWUP_MESSAGE = (
    "Hello {first_name},\n\n"
    "I haven't gotten your feedback from the link I sent to you earlier today.\n\n"
    "Just wanted to know if you were able to go through it?"
)


# ============================================================
# How long (in hours) to wait before sending the follow-up
# ============================================================
FOLLOWUP_HOURS = 1