Init:

- Open rental order "S00028" and cancel it
- Open the sale "Rental > Schedule > Schedule"
- Show list view and ensure 9 lines are shown

Move period:

- Open the sale "Rental > Schedule > Check Period"
- Select start date previous week and click "Adjust Period"
- Check if placeholder lots have been moved

New lot:

- Create lot "PRINT005" for "Printer"
- Add qty 1 to lot
- Ensure new slot is created

Filer:

- Open the sale "Rental > Schedule > Schedule"
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
- Save and set qty to 2
- Ensure slots have been recreated
- Click on the smart button
- Extend the end date
- Open slot and click "View Rental Order"

Check avilaiblity:

- Open the sale "Rental > Schedule > Check Period"
- Set start and end date to tomorrow and day after tomorrow
- Click "View Availability"
- Ensure only 3 slots are available for "Printer"

Create additional rental order:

- Duplicate the previous order
- Confirm and pickup "PRINT001" and "PRINT005" lot
- Click smart button and remove order filter
- Ensure the view is correct
- Return to duplicated order and try to cancel it.

Partial return:

- Execute a return for "PRINT001" lot
- Ensure only 2 slots are shown and are linked correctly
- Return the remaining slot
- Cancel the order
- Ensure the slots are gone
