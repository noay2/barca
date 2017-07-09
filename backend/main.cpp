
#include <iostream>
#include "Generic_Board.hpp"
#include "User_Interface.hpp"

int main(int argc, const char * argv[]) {
    Board * bob =  new Board();
    User_Interface ui = User_Interface(bob);

    while(!bob->exists_victory)
    {
        ui.print_board();
        ui.turn();
    }
    ui.print_board();

    std::cout<<"Victory"<<std::endl;
    delete bob;
    return 0;
}
