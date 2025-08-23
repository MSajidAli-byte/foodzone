# Dashboard

This page documents the authenticated user Dashboard template in the FoodZone project and its tabbed functionality.

- Template: `template/dashboard.html`
- Purpose: Provide a central place for users to view their profile summary, edit profile details, change password, review order history, and log out.

## Screenshot

![Dashboard](img/dashboard.png)

## Tabbed Interface

The dashboard uses a tab-pane pattern (Bootstrap tabs) to switch between sections without leaving the page.

- Navigation tabs (anchors) reference corresponding pane IDs via `href="#..."` and `data-toggle="tab"`.
- Content panes are defined with `.tab-pane` containers.
- The active pane is marked with `.active`.

### Tabs available

1) Dashboard
- Displays user summary:
  - Profile picture (or a circular avatar with the user’s first initial if no picture is set)
  - Name and email
  - Contact number
  - Member since (date joined)
  - Last login time

2) Edit Profile
- Form fields (with CSRF protection):
  - Name (editable)
  - Email (readonly)
  - Contact Number (11 digits, validated via a pattern)
  - Address (textarea)
  - Profile Picture (file upload)
- Submit button name: `update_profile`
- Expected behavior: POSTs to the same view; upon success, the page may show an alert via `status` in context.

3) Change Password
- Form fields (with CSRF protection):
  - Current Password
  - New Password
  - Repeat New Password
- Client-side password match check:
  - A small script toggles the submit button’s disabled state and updates a message if passwords don’t match.
- Submit button name: `change_pass`

4) My Orders
- Lists historical orders with:
  - Dish image, name, and discounted price
  - Invoice ID and ordered date
  - Status badge: Successful, Failed/Cancelled, or Pending
- Each order item links to its dish details page.
- The nav tab shows a badge with the total number of orders: `({{ orders|length }})`.

5) Logout
- A simple link to `{% url 'logout' %}` that signs the user out.

## Implementation Notes

- Tabs
  - Nav: `ul.nav.nav-tabs > li.nav-item > a.nav-link` with `data-toggle="tab"` and `href` pointing to the pane ID.
  - Panes: `div.tab-content > div.tab-pane` with matching IDs, e.g. `#dash`, `#edit`, `#cpass`, `#orders`.
  - Requires Bootstrap’s JS (and its dependencies) for tab switching.

- Profile Image Fallback
  - If `profile.profile_picture` exists, show the uploaded image.
  - Otherwise render a circular avatar with the user’s first initial: `{{ profile.user.first_name.0 }}`.

- Feedback Messages
  - A context variable `status` triggers a JavaScript `alert` to notify users of successful actions.

## Access and Security

- This page should be restricted to authenticated users (e.g., via `@login_required` in the corresponding view).
- Typically reachable via a route such as `/dashboard/` with the URL name `dashboard` (exact URL name may vary).

## Additional Images (Optional)

For documentation granularity, you may include tab-specific screenshots:

- Edit Profile: ![Edit Profile](img/dashboard_edit_profile.png)
- Change Password: ![Change Password](img/dashboard_change_pass.png)
- My Orders: ![My Orders](img/dashboard_my_orders.png)
- My Orders: ![My Orders](img/dashboard_my_orders_modal form.png)
- My Orders: ![My Orders](img/dashboard_my_orders_cleared entry.png)

## Tips

- Ensure Bootstrap CSS/JS are included so tabs function properly.
- Validate user inputs server-side in addition to any client-side checks.
- When updating profile details, handle file uploads correctly (`enctype="multipart/form-data"`).
