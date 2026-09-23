Setup:

- Open rental order "S00028" and cancel it
- Open the sale "Rental > Schedule > Schedule"
- Show list view and ensure 5 lines are shown
- Remove filter "Has Order Lines" and ensure 4 lines are added

Move period:

- Open the sale "Rental > Schedule > Check Period"
- Select start date previous week and click "Adjust Period"
- Check if placeholder lots have been moved

Split order line:

- Open slot of "S00023"
- Click "Split Order Line"
- Enter 1.0 and split
- There must be two lines now

New lot:

- Open "Printer" qty and create new lot "PRINT005" with qty 1.0
- Open lot and ensure new placeholder slot is created

Filer:

- Open the sale "Rental > Schedule > Schedule"
- Then search for "acme"
- Ensure there are 3 slots
- Apply filter "Placeholder"
- Search for "Print"
- Ensure there are 5 slot

Create rental order:

- Open a placeholder slot
- Click "Create Rental Order" for "Acme Corporation"
- Set dates to tomorrow and day after tomorrow
- Set qty to 2 and save
- Ensure slots have been recreated
- Try to set qty 6, you must get an error

Check view:

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
- Ensure the view shows all order and correct colors

Check available lots

- Move the order in pickup state after the other
- Open the pickup order and confirm it
- Click "Pickup" and make sure that "PRINT001" can be selected
