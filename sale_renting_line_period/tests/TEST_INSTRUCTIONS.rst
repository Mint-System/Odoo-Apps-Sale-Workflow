
Setup:

- Open rental order "S00021"
- Change start date to next monday and return date friday after monday
- Check if dates are updated on products
- Confirm the order
- Click on pickup and validate both lines

Partial return:

- Click return
- For conference room set 0.0
- For pojector set 2.0
- Select return date 2 days after start date
- Click apply
- Check if Odoo splitted the line into two lines

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
