import requests
import json

def get_new_deck():
    response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=2")
    
    return json.loads(response.text)["deck_id"]

def draw_cards(deck_id, count):
    response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}")
    return json.loads(response.text)["cards"]

def calculate_hand_value(cards):
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'JACK': 10, 'QUEEN': 10, 'KING': 10}
    aces = 0
    total_value = 0

    for card in cards:
        rank = card['value']
        if rank == 'ACE':
            aces += 1
        else:
            total_value += values[rank]

    for _ in range(aces):
        if total_value + 11 <= 21:
            total_value += 11
        else:
            total_value += 1

    return total_value

def show_hand(cards):
    for card in cards:
        print(f"{card['value']} of {card['suit']}")

def play_game(deck_id):
    player_hand = draw_cards(deck_id, 2)
    dealer_hand = draw_cards(deck_id, 2)

    print("Your hand:")
    show_hand(player_hand)
    print("Dealer's hand:")
    print(f"{dealer_hand[0]['value']} of {dealer_hand[0]['suit']}")
    
    while True:
        action = input("Do you want to h = 'hit' or s = 'stand'? ('q' to quit) ").lower()
        
        if action == 'q':
            break
        elif action == 'h':
            player_hand.extend(draw_cards(deck_id, 1))
            print("Your hand:")
            show_hand(player_hand)
            if calculate_hand_value(player_hand) > 21:
                print("Bust! You lose.")
                break
        elif action == 's':
            while calculate_hand_value(dealer_hand) < 17:
                dealer_hand.extend(draw_cards(deck_id, 1))
            print("Your hand:")
            show_hand(player_hand)
            print("Dealer's hand:")
            show_hand(dealer_hand)
            
            player_value = calculate_hand_value(player_hand)
            dealer_value = calculate_hand_value(dealer_hand)
            
            if player_value > 21:
                print("Bust! You lose.")
            elif dealer_value > 21 or player_value > dealer_value:
                print("Congratulations! You win.")
            elif player_value < dealer_value:
                print("You lose.")
            else:
                print("It's a tie.")
                
            break

def main():
    deck_id = get_new_deck()
    print("*$*$*$*$*$Play a hand of Blackjack*$*$*$*$*$")
    
    while True:
        play_again = input("Do you want to play a game? (y = yes/q = no) ").lower()
        if play_again != 'y':
            break
        
        play_game(deck_id)

if __name__ == "__main__":
    main()
