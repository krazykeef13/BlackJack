import requests

def create_new_deck():
    response = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=4')
    deck_id = response.json()['deck_id']
    return deck_id

def draw_cards(deck_id, num_of_cards):
    response = requests.get(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={num_of_cards}')
    cards = response.json()['cards']
    return cards

def calculate_hand_value(hand):
    value = 0
    for card in hand:
        card_value = card['value']
        if card_value in ['KING', 'QUEEN', 'JACK']:
            value += 10
        elif card_value == 'ACE':
            value += 11
        else:
            value += int(card_value)
    for card in hand:
        if card['value'] == 'ACE' and value > 21:
            value -= 10
    return value

def display_player_hand(player_hand):
    print("Your hand:")
    for card in player_hand:
        print(f"{card['value']} of {card['suit']}")
    print(f"Your hand value: {calculate_hand_value(player_hand)}")

def display_dealer_hand(dealer_hand):
    print("Dealer's hand:")
    print(f"{dealer_hand[0]['value']} of {dealer_hand[0]['suit']}")
    print("Hidden card")

def player_turn(deck_id, player_hand):
    while True:
        action = input("Do you want to hit (h) or stand (s)? ").lower()
        if action == 'h':
            card = draw_cards(deck_id, 1)[0]
            player_hand.append(card)
            print(f"You drew: {card['value']} of {card['suit']}")
            display_player_hand(player_hand)
            if calculate_hand_value(player_hand) > 21:
                print("Bust! You lose.")
                break
        elif action == 's':
            break
        else:
            print("Invalid input. Please enter 'h' for hit or 's' for stand.")

def dealer_turn(deck_id, dealer_hand):
    print("Dealer's turn:")
    display_dealer_hand(dealer_hand)
    while calculate_hand_value(dealer_hand) < 17:
        card = draw_cards(deck_id, 1)[0]
        dealer_hand.append(card)
        print(f"Dealer drew: {card['value']} of {card['suit']}")
        display_dealer_hand(dealer_hand)
        if calculate_hand_value(dealer_hand) > 21:
            print("Dealer busts! You win.")
            break

def determine_winner(player_hand, dealer_hand):
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if player_value > 21 or (dealer_value <= 21 and dealer_value > player_value):
        print("Dealer wins!")
    elif dealer_value > 21 or player_value > dealer_value:
        print("You win!")
    else:
        print("It's a tie!")

def main():
    deck_id = create_new_deck()

    while True:
        player_hand = draw_cards(deck_id, 2)
        dealer_hand = draw_cards(deck_id, 2)

        print("$*$*$*$*PLAY BLACKJACK*$*$*$*$")
        display_player_hand(player_hand)
        display_dealer_hand(dealer_hand)

        player_turn(deck_id, player_hand)

        if calculate_hand_value(player_hand) <= 21:
            dealer_turn(deck_id, dealer_hand)

        determine_winner(player_hand, dealer_hand)

        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            break

if __name__ == "__main__":
    main()
