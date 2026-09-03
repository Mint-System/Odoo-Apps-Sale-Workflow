Unpaid subscription:

- Enable the module.
- Create or edit sale subscription order.
- Create unpaid invoice with date in the past.
- Run scheduled action "Sale Subscription: subscriptions expiration".
- Check that order is not closed.

Expired synscriptions:

- Create or edit sale subscription order.
- Chose recurring plan "Monthly"
- Set Automatic Closing of this plan to 5 days.
- Set next invoice date to date older than 5 days from today.
- Run scheduled action "Sale Subscription: subscriptions expiration".
- Check that order is not closed.
