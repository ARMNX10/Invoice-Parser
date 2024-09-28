import Parser

# Parser.set_pdf("test_pdfs/09232024_WHOLESALE.pdf")
Parser.set_pdf("test_pdfs/invoice.pdf")

Parser.query("set quantity_minimum = 2")
Parser.query(
    "select keys from words as word where 180 < word.center.x < 200 and word.center.y > 800"
)
Parser.query(
    "select prices from words as word where 1000 < word.center.x < 1200 and 1100 > word.center.y > 800"
)
# Parser.query(
#     "select quantities from keys as key where int(key.text) > quantity_minimum"
# )
Parser.query(
    "select amounts from words as word with keys as key where 1400 < word.center.x < 1500 and -20 < (key.center.y - word.center.y) < 20"
)
Parser.query("export keys as keys")
Parser.query("export amounts as amounts")
Parser.query("export prices as prices")





# For invoice1.pdf

# Parser.query(
#     "select item from words as word where 257 < word.center.x < 385 and 541 < word.center.y and word.page == 0"
# )
# Parser.query("export item as items")






Parser.query("end")
