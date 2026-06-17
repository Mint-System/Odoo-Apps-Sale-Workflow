Add product:

- Open rental order "S00021"
- Search for "Projector" and and remove the item

Pickup:

- Open rental order "S00028" and abort
- Open rental order "S00021"
- Change start date to next monday and return the following
- Check if dates are updated on products
- Confirm the order
- Click on pickup and validate both lines
- Select all lots for printer

Partial return:

- Click return
- For conference room set 0.0
- For printer remove "PRINT003"
- Select return date 2 days after start date
- Click validate
- Check if Odoo splitted the line into two lines
- Check if the lots are assigned correctly

Extend period:

- Change the return date of the order to plus 1 week
- Ensure return date is updated for line not in state returned
- Check if price calculation is correct

Return remaining:

- Click return
- Check if all lines have been returned

Invoice:

- Create invoice for rental order
- Ensure the period descriptions are correct
