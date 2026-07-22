Init:

- Open rental order "S00028" and cancel it
- Open the sale "Rental > Schedule > Availability"
- Show list view and ensure 6 lines are shown

New lot:

- Create lot "PRINT005" for "Printer"
- Add qty 1 to lot
- Ensure new slot is created

Filer:

- Apply filter "Has Order Line"
- Then search for "acme"
- Ensure there is 1 slot
- Apply filter "Unlinked Lot"
- Search for "Print"
- Ensure there are 5 slot

Edit:

- Drag and drop line of "S00023" so end date is past
- Ensure the start and end date is updated

Check Period:

- Open the sale "Rental > Schedule > Filter Period"
- Filter from tomorrow to day after tomorrow.
- Click View Gantt
- Open one of the printer slots

Create rental order:

- Click "Create Rental Order"
- Set dates to tomorrow and day after tomorrow
- Confirm the order
- Click on the smart button and remove filter
- Click on slot, edit and select "Show Rental Order"
- Go back to order and pickup "PRINT005" lot

Check period again:

- Open the sale "Rental > Schedule > Filter Period"
- Filter from tomorrow to day after tomorrow.


Cancel rental order:
