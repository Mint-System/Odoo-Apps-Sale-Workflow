Init:

- Open rental order "S00028" and cancel it
- Open the sale "Rental > Schedule > Availability"
- Show list view and ensure 9 lines are shown

New lot:

- Create lot "PRINT005" for "Printer"
- Add qty 1 to lot
- Ensure new slot is created

Filer:

- Open the sale "Rental > Schedule > Availability"
- Apply filter "Has Order Line"
- Then search for "acme"
- Ensure there are 3 slots
- Apply filter "Placeholder"
- Search for "Print"
- Ensure there are 5 slot

Create rental order:

- Open a placeholder slot
- Click "Create Rental Order"
- Set dates to tomorrow and day after tomorrow
- Set qty to 2
- Confirm the order
- Click on the smart button
- Extend the end date
- Click on slot and "View Rental Order"

Create additional rental order:

- Duplicate the order
- Confirm and pickup "PRINT001" and "PRINT005" lot
- Open "Availability" and filter "Printer"
- Ensure the view is correct
- Open the new order, cancel it and return to view
- Ensure the slots are gone

Partial return:

- Open the original order
- Confirm and pickup "PRINT001" and "PRINT005" lot
- Execute a return for "PRINT001" lot
- Ensure only 2 slots are shown and are linked correctly
