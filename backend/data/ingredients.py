# ingredient -> (helps concerns, bad for skin types, plain-language note)
INGREDIENTS = {
    "niacinamide": (["Acne", "Dark spots", "Redness"], [], "Calms redness and evens tone."),
    "salicylic acid": (["Acne"], ["Dry/Normal"], "Unclogs pores, but can dry out already-dry skin."),
    "hyaluronic acid": (["Dryness"], [], "Pulls water into the skin."),
    "ceramide": (["Dryness", "Redness"], [], "Repairs the skin barrier."),
    "vitamin c": (["Dark spots"], [], "Brightens and fades pigmentation."),
    "retinol": (["Acne", "Dark spots"], [], "Boosts renewal; irritating if skin is sensitive."),
    "benzoyl peroxide": (["Acne"], ["Dry/Normal"], "Kills acne bacteria; very drying."),
    "glycolic acid": (["Dark spots"], ["Dry/Normal"], "Exfoliates; can sting dry or sensitive skin."),
    "alcohol denat": ([], ["Dry/Normal", "Combination"], "Strips natural oils."),
    "fragrance": ([], [], "A common trigger for allergies and irritation."),
    "parfum": ([], [], "A common trigger for allergies and irritation."),
    "coconut oil": ([], ["Oily", "Combination"], "Heavy and pore-clogging for oily skin."),
    "isopropyl myristate": ([], ["Oily"], "Known to clog pores."),
    "aloe": (["Redness", "Dryness"], [], "Soothes and hydrates."),
    "tea tree": (["Acne"], [], "Mild antibacterial; can irritate in high amounts."),
}
CONFLICTS = [({"retinol"}, {"glycolic acid", "salicylic acid", "benzoyl peroxide", "vitamin c"},
              "Retinol with strong acids or peroxide can over-exfoliate. Use on alternate nights."),
             ({"vitamin c"}, {"benzoyl peroxide"}, "Benzoyl peroxide can deactivate vitamin C.")]
