Add product:

- Open rental order "S00021"
- Add line with "Projector" and save
- Check if name is correct
- Remove the line

Pickup:

- Open rental order "S00028" and cancel it
- Open rental order "S00021"
- Change start date to 2 days ago and return to next friday
- Check if dates are updated on products
- Confirm the order
- Click on pickup
- Select all lots for printer
- And validate

Return not lot:

- Click return
- For conference set return date 1 day after start date
- Remove print from return list
- Validate and check if return date is set correctly

Split line:

- Click on split line action
- Enter 1.0
- Ensure a new line with qty 1.0 is created
- Check if the lots have been transfered

Partial return with lot:

- Click return
- Remove the line with only 1 lot
- Select return date 2 days after today
- Click validate

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

- Change start date to next monday and return to friday
- Confirm the order
- Click on pickup and select "PRINT001" lot
- Click validate
- Duplicate the new order and confirm
- Click on pickup and ensure that "PRINT001" is not available
- Change start and end date to plus one week
- Click on pickup and ensure that "PRINT001" is available
