### Requirements
1. Read inventory from **tu_vending_inventory.json** (the price_usd is the price in US Dollars $)
2. Assign the inventory to a Vending Location (Grid layout A1, A2, A3, A4, A5, B1, B2, B3..etc...there are 30 items in the inventory, so a grid of 5x6 or 6x5 works nicely)
3. Interactive vending machine, continues until user quits
4. Sell items, keeping track of available inventory.
5. You can't sell items that are out of stock (0 inventory)
6. When the user quits, print out the sales total as part of the goodbye message
7. Saves the ending inventory status (to *orginal* json **format** (it doesn't have to be the same actual file, but it could be) or database)
8. Saves the list of transactions to CSV file OR to Database. Your CSV header row *might* look like this:

    `SLOT_ID,AMOUNT_USD,ITEM`
9. Has at least two (2) Unit Tests that tests a component that you have written 
(could be testing that the currency exchange rate calculation was done correctly, or that when a transaction is done, it is correctly stored in your transaction log, or tests that when an item is sold, it is correctly accounted for in your virtual vending machine, or makes sure the total does not increase when an out of stock item is purchased)