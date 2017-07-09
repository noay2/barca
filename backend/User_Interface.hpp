

#ifndef User_Interface_hpp
#define User_Interface_hpp

#include <stdio.h>
#include <utility>
#include <string>
#include "Generic_Board.hpp"


class User_Interface
{
public:
    User_Interface(Board* board)
    {
        this->board = board;
        
    }
    
    void turn()
    {
        this->ask_user();
        this->make_move();
    }
    
    void ask_user()
    {
        this->valid_piece = false;
        this->valid_destination = false;
        this->validmoves.clear();

        while(!this->valid_destination)
        {
            this->valid_piece = false;
            this->valid_destination = false;
            this->validmoves.clear();
            while(!this->valid_piece)
            {
                std::cout<<"Please Select the Location of the Piece You Would Like to Move"<<std::endl;
                std::cout<<""<<std::endl;
                std::getline (std::cin,this->piece);
                check_piece_selection();
            }
            std::cout<<""<<std::endl;
            std::cout<<"Please Select the Location Where You Would Like to Move the Piece"<<std::endl;
            std::cout<<""<<std::endl;
            std::getline (std::cin,this->destination);
            check_piece_destination();
            
            
            
        }

    }
    
    void check_piece_selection()
    {
        std::size_t location = this->piece.find(" ");
        if( (location != std::string::npos) )
        {
            try
            {
                this->piece_location[0] = std::stoi(piece.substr(0,location)) -1;
                this->piece_location[1] = std::stoi(piece.substr(location+1, this->piece.length() - (location +1)))-1;
                
                if( (this->piece_location[0] >=0) && (this->piece_location[0] < this->board->rows) &&
                    (this->piece_location[1] >=0) && (this->piece_location[1] < this->board->cols)
                   )
                {
                    this->board->validmoves(this->validmoves, piece_location);
                
                    if ( int (this->validmoves.size()) > 0 )
                    {
                     //   for(auto i = this->validmoves.begin(); i != this->validmoves.end(); ++i)
                     //       {std::cout<<(i->first) +1<<" "<<(i->second) +1<<std::endl;}
                        this->valid_piece = true;
                        return;
                    }
                }
                    
            }
            catch( std::exception & e){}
        }
        std::cout<<""<<std::endl;
        std::cout<<"Please Type the Location of a Valid Piece"<<std::endl;
    }
    
    void check_piece_destination()
    {
        std::size_t location = this->destination.find(" ");
        if( (location != std::string::npos) )
        {
            try
            {
                this->destination_location[0] = std::stoi(this->destination.substr(0,location)) -1;
                this->destination_location[1] = std::stoi(this->destination.substr(location+1, this->destination.length() - (location +1)))-1;
                
                if( (this->destination_location[0] >=0) && (this->destination_location[0] < this->board->rows) &&
                   (this->destination_location[1] >=0) && (this->destination_location[1] < this->board->cols)
                   )
                {
                    for (auto i = this->validmoves.begin(); i != this->validmoves.end(); ++i)
                    {
                        if (   ((*i).first == destination_location[0]) && ((*i).second == destination_location[1])  )
                        {
                            this->valid_destination = true;
                            return;

                        }
                    }
                }
                
            }
            catch( std::exception & e){}
        }
        std::cout<<""<<std::endl;
        std::cout<<"Destination was Not Recognized"<<std::endl;
        
    }
    
    void make_move()
    {
        this->board->make_move(board->board[piece_location[0]][piece_location[1]], destination_location[0], destination_location[1]);
    }

    void print_board()
    {
        std::cout<<""<<std::endl;
        std::cout<<"   ";
        for(int i = 1; i != 11; ++i)
        {
            std::cout<<i;
            std::cout<<"   ";
        }
        
        
        
        std::cout<<std::endl<<std::endl;
        for (int i = this->board->rows-1; i>=0; --i)
        {
            std::cout<<i+1<<" ";
            if (i+1!= 10)
            {std::cout<<" ";}
            for (int j = 0; j< this->board->cols; ++j)
            {
                
                if (this->board->board[i][j] == nullptr)
                {
                    std::cout<<"--";
                }
                else
                {
                    Piece* temp =  this->board->board[i][j];
                    std::cout<< temp->color [0];
                    std::cout<< temp->type  [0];
                }
                std::cout<<"  ";
                
            }
            std::cout<<std::endl<<std::endl;
        }
        
        
        
        
        std::cout<<"   ";
        for(int i = 1; i != 11; ++i)
        {
            std::cout<<i;
            std::cout<<"   ";
        }
        std::cout<<std::endl;
    }
    
    
    
    
    Board * board = nullptr;
    
    bool valid_piece;
    std::string piece;
    int piece_location [2];
    
    std::vector<std::pair<int, int>> validmoves;
    
    bool valid_destination;
    std::string destination;
    int destination_location[2];
    

};

#endif /* User_Interface_hpp */
