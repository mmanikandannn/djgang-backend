# Admin Implementation Notes

Statistics are calculated from the actual models in `accounts`, `bookings`, `catalog`, `orders`, `events_app`, `gallery`, and `music`. Analytics and management views use `staff_member_required`. The standard Django admin is retained to preserve permissions, search, filters, inline order items, product images, and all existing model registrations.
