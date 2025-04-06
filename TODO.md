# TODO:

## High priority:
- [ ] Have to fix the loading screen! When you submit the user account, it takes a second! Use HTMX loading (like in the reddit example) to give it modern feel while it works async.
- [ ] Fix Tailwind in production (maybe use django-tailwind?)
- [ ] Hook-up shopify!
  - [ ] Fill in the storefront
  - [ ] Wire up the shopify webhooks so that we can listen to the changes to user subscriptions, purchases, etc.
  - [ ] This stuff has to be *great* -- it's really the core of the app.
- [ ] Add more models:
  - [ ] Model "subscription" on backend
  - [ ] "content", which can be academic paper, essay, blog post, etc.
    - [ ] content has an author
    - [ ] content has flag(s)
  - [ ] "user_preferences"
    - [ ] "ai_preference" -- allow users to opt in or out of AI / ML-heavy content.
      - [ ] This is sort of a gimmick, and it's silly to only have one control, but we're going to start there.
      - [ ] In the future, we could further customize user preferences and send content based on their preferences, but we want to be very careful, and keep Papers "boring".
  - [ ] We can keep track of whether or not an email has received a piece of content, to avoid repeats
  - [ ] "envelope" is a collection of "content"
  - [ ] We always need to have a queue of "envelopes" for our oldest, most reliable customers
    - [ ] Users which are newer, or have paused their subscription, can receive previous envelopes, as long as they haven't received that content before
  - [ ] 

## Medium priority:
- [ ] Add subscription pausing instead of cancelling(?)
- [ ] Set up a cleanup cronjob for webhook logs

## Low priority:
- [ ]


## Pages
- Homepage (Landing Page)
- Subscription page
- Subscription management page
  - Add