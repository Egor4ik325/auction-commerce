# Auction e-commerce

E-commerce website for making bids on created auctions.

## Roadmap

- [x] listings
- [x] bids
- [x] comments
- [x] watchlist
- [x] deploy
- turn into production-ready
   - [x] static files
   - [x] DEBUG=False
   - [x] HTTPs certificate
- [ ] ebay-like
- [ ] win
- [ ] 3-d party package
- [ ] user profile

## Specification

Auction terms:
- Auction - process of selling listing (one or multiple)
- Listing - listing about some item
- Item - item that is placed on auction
- Bid - atemp to win an listing (item) by placing money (setting price)

Database schema:

- User
    * Name
    * Phone
    * Mail
    * Money
    * Card
- Listing
- Bid

### User flow

1. Post listing with starting price
2. Other users take bids
3. User with higher bid wins in the end second
4. Users pays money

### Additional fields

- rating/feedback
- payment option
- register date
- shipping
- delivery
- payments
- returns
