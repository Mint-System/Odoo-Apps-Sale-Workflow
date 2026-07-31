Add product:

- Open rental order "S00021"
- Search for "Projector" add and remove the item
- Check if name is correct

Pickup:

- Open rental order "S00028" and cancel it
- Open rental order "S00021"
- Change start date to yesterady and return to next friday
- Check if dates are updated on products
- Confirm the order
- Click on pickup
- Select all lots for printer
- And validate

Return not lot:

- Click return
- For conference set return date 1 day after start date
- Remove all selected lots for pinter
- Validate and check if return date is set correctly

Partial return with lot:

- Click return
- Ensure conference room is not shown
- For printer remove "PRINT003"
- Select return date 2 days after today
- Click validate
- Check if Odoo splitted the line into two lines
- Check if the lots are assigned correctly and cannot be edited

Extend period:

- Change the return date of the order to plus 1 week
- Ensure return date is updated for remaining line not in state returned
- Check if price calculation is correct

Return remaining:

- Click return
- Check if all lines have been returned

Invoice:

- Create invoice for rental order
- Ensure the period descriptions are correct

Check availability:

- Cancel "S00021" and duplicate "S00021"
- Remove all lines execept 1 printer
- Change start date to next monday and return to friday
- Confirm the order
- Click on pickup and select "PRINT001" lot
- Click validate
- Duplicate the new order and confirm
- Click on pickup and ensure that "PRINT001" is not available
- Change start and end date to plus one week
- Click on pickup and ensure that "PRINT001" is available
