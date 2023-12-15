#include <cctype>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <iterator>
#include <ostream>
#include <string>
#include <vector>

/*
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
*/

struct card {
    std::vector<int> win_num;
    std::vector<int> my_num;
    int card_number;
    int instances;
};

struct cards {
    std::vector<card> cards_;
};

struct tuple {
    std::string win_num;
    std::string my_num;
};

std::vector<card> _cards;

tuple get_tuple(const std::string &line) {
    size_t start_index = line.find(':');
    size_t sperator = line.find('|');
    struct tuple _tuple;
    std::string num1 = "";
    std::string num2 = "";
    for (int i = start_index + 1; i < line.size(); ++i) {
        if (i < sperator)
            num1 += line.at(i);
        if (i > sperator)
            num2 += line.at(i);
    }
    _tuple.win_num = num1;
    _tuple.my_num = num2;
    return _tuple;
}

std::vector<int> construct_array(const std::string &line) {
    std::vector<int> arr;
    std::string num = "";
    for (int i = 0; i < line.size(); i++) {
        if (std::isdigit(line.at(i))) {
            num += line.at(i);
        } else if (std::isspace(line.at(i)) && !num.empty()) {
            int n = std::stoi(num);
            arr.push_back(n);
            num.clear();
        }
    }
    if (!num.empty()) {
        int n = std::stoi(num);
        arr.push_back(n);
        num.clear();
    }
    return arr;
}

card construct_card(const std::string &line, int card_number) {
    tuple t = get_tuple(line);
    card _card;
    _card.win_num = construct_array(t.win_num);
    _card.my_num = construct_array(t.my_num);
    _card.card_number = card_number;
    _card.instances = 1;
    return _card;
}

int calculate_points(const card *c) {
    int pts = 0;
    for (int i = 0; i < c->win_num.size(); i++) {
        int current = c->win_num.at(i);
        for (int j = 0; j < c->my_num.size(); j++) {
            if (current == c->my_num.at(j)) {
                pts = pts == 0 ? 1 : pts * 2;
            }
        }
    }
    return pts;
}

// makeCopy(currenCardNumber, numberOfMatches) -> increament each card instance by 1
void make_copies(int current_card_number, int numbers_of_matches) {
    // make sure that current_card_number is equals to the index of the desired number not the printed N.
    std::cout << "Card " << current_card_number + 1 << " will make a copy of the next " << numbers_of_matches
              << " cards \n";
    for (int i = current_card_number + 1; i <= current_card_number + numbers_of_matches && i < _cards.size(); i++) {
        _cards.at(i).instances++;

        // print report:
        std::cout << "A copy of card " << _cards.at(i).card_number << " was made by card " << current_card_number + 1
                  << "\n";
    }
}

// calculateNumberOfMatches(currentCard) -> returns total N. matches
int calculate_number_of_matches(const card *current_card) {
    int number_of_matches = 0;
    // card current_card = _cards.at(number_of_matches);
    // a loop to go through the win numbers
    for (int i = 0; i < current_card->win_num.size(); i++) {
        int current_win_num = current_card->win_num.at(i);
        // a loop to go through my numbers and then compare them
        for (int j = 0; j < current_card->my_num.size(); j++) {
            if (current_win_num == current_card->my_num.at(j)) {
                number_of_matches += 1;
            }
        }
    }
    return number_of_matches;
}

int solve(const std::string &path) {
    std::ifstream file;
    file.open(path);
    if (!file.is_open()) {
        return 0;
    }
    std::string line;
    // int sum = 0;
    int card_number = 1;
    // This loop will save all card in _cards array
    while (std::getline(file, line)) {
        auto c = construct_card(line, card_number++);
        // save card in _cards array:
        std::cout << "Card constracted: card " << c.card_number << "\n";
        _cards.push_back(c);

        // sum += calculate_points(&c);
    }

    // This loop will go through the _cards array to find number of instances and calculate the scratchcards
    for (int i = 0; i < _cards.size(); i++) {
        auto currentCard = _cards.at(i);
        int matches_num = calculate_number_of_matches(&currentCard); // minus 1 to match the index
        // a loop to re-play card (instances) times and find number of instances and calculate the scratchcards
        for (int j = 0; j < currentCard.instances; j++) {
            make_copies(currentCard.card_number - 1, matches_num);
        }
    }

    int scratchcards = 0;
    // A loop to calc the number of scratchcards
    for (int i = 0; i < _cards.size(); i++) {
        scratchcards += _cards.at(i).instances;
    }
    return scratchcards;
}

int main() {
    std::cout << "total scratchcards = " << solve("./input.txt") << "\n";

    return 0;
}


