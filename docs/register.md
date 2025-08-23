# Register Page

This page documents the user registration flow and template in the FoodZone project.

- Template: `template/register.html`
- View: `foodapp.views.register`
- Purpose: Allow new users to create an account with name, email, password, and contact number.

## Screenshot

![Register page](img/register.png)

## How to Access

- From the site’s navigation bar, clicking the user/account icon will open the Register page.
- Alternatively, navigate directly to the route named `register` (e.g., `/register/` if configured that way).

## Backend Logic

The `register` view supports both GET and POST:

- GET: Renders the registration form.
- POST: Accepts the following fields and performs validation and user creation.
  - `name`
  - `email` (used as the username)
  - `pass` (password)
  - `number` (contact number)

On success, it creates:
- A Django `User` with `username=email`
- A related `Profile` with the provided contact number

If a user with the same email already exists, an error is returned.

Rough flow:

```python
if request.method == "POST":
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    contact = request.POST.get('number')

    check = User.objects.filter(username=email)
    if len(check) == 0:
        usr = User.objects.create_user(email, email, password)
        usr.first_name = name
        usr.save()

        profile = Profile(user=usr, contact=contact)
        profile.save()

        context['status'] = f"User {name} Registered Successfully!"
    else:
        context['error'] = "A User with this email already exists"
```

## Template Expectations

Form fields expected in `register.html`:
- `name`: text input
- `email`: email input
- `pass`: password input
- `number`: text input for contact number

Include CSRF token and post to the `register` URL name:

```html
<form method="post" action="{% url 'register' %}">
  {% csrf_token %}
  <!-- name, email, pass, number fields -->
  <button type="submit" class="btn custom-btn">Register</button>
</form>
```

## UX Notes

- Display `context['status']` as a success message and/or redirect after successful registration.
- Display `context['error']` when a user already exists.
- The navbar user icon should link to `{% url 'register' %}` so users can easily find the Register page.
