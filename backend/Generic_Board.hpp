

#ifndef Board_hpp
#define Board_hpp

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <utility>
#include <string>
#include "Generic_Piece.hpp"


class Board

{
public:

    Board()
    {
        this->exists_victory = false;
        this->turn    = "WHITE";
        this->board  = std::vector<std::vector<Piece *>> ();
        this->Pieces = std::vector<Piece>();
        //this->moves_chronological = std::vector< std::pair< Piece *,int [2][2]> > ();
        //this->afraid_trapped_safe_chronological = std::vector< std::vector<std::pair< Piece *,std::string [2]> >> ();
        
        for (int i = 0; i < this->rows; ++i)
        {
            this->board.push_back(std::vector<Piece*> ());
            for (int j = 0; j < this->cols; ++j)
            {
                this->board[i].push_back(nullptr);
            }
        }
        

        
        int counter = 0;
        for (int i = 0;  i< 2; ++i)
        {
            for (int j = 0 ; j<3; ++j)
            {
                for (int k = 1; k<3; k++)
                {
                    this->Pieces.push_back(Piece(this->colors[i], this->types[j], k,
                                           this->initial_piece_locat[counter][0], this->initial_piece_locat[counter][1],
                                           &this->turn,&this->board, &this->Pieces
                                          ));
                    counter +=1;
                }
            }
        }
        for(auto piece = Pieces.begin(); piece != Pieces.end(); piece++)
        {
            this->board[piece->row][piece->col] = & *piece;
            
        }
        
        

        

    }

    
    
    void validmoves(std::vector<std::pair<int, int>> & validmoves, int * piece_location)
    {
        Piece * piece = this->board[piece_location[0]][piece_location[1]];

        if (piece == nullptr || piece->color !=  this->turn)                   //Not Piece's/NULL's move
        {
            return;
        }
        piece->validmoves(validmoves);
        
    }
    
    

    
    
    void check_victory()
    {
        int white_counter = 0;
        int black_counter = 0;
        for (int i = 0; i<4; ++i)
        {
            Piece* temp = this->board[watering_holes[i][0]][watering_holes[i][1]];
            if (temp != nullptr)
            {
                if (temp->color == "WHITE")
                {white_counter +=1;}
            
                else if(temp->color =="BLACK")
                {black_counter +=1;}
            }
        }
        this->exists_victory =  white_counter>=3 || black_counter >=3;
    }
    
    
    void switch_turn()
    {
        if(! this->exists_victory)
        {
            if (this->turn =="BLACK")
            {
                this->turn = "WHITE";
            }
            else if (this->turn =="WHITE")
            {
                this->turn = "BLACK";
            }
        }
    }

    
    void make_move(Piece * piece, int row, int col)
    {
        this->board[piece->row][piece->col] = nullptr;
        this->board[row][col] = piece;
        piece->row = row;
        piece->col = col;
        
        piece->fear_update();
        
        this->check_victory();
        this->switch_turn();
        
        
    }
    
    bool exists_victory;
    std::string turn = "WHITE";
    std::vector<std::vector<Piece*>> board;
    std::vector<Piece> Pieces;
    

    int rows = 10;
    int cols = 10;
    std::string colors[2] = {"BLACK", "WHITE"};
    std::string types[3]  = {"ELEPHANT", "MOUSE", "LION"};
    
    
    
    
    int watering_holes [4][2] = { {this->rows/2 -2, this-> cols/2 -2},{this->rows/2 -2, this-> cols/2 +1},
                                  {this->rows/2 +1, this-> cols/2 -2}, {this->rows/2 +1, this-> cols/2 +1}
                                };
    int initial_piece_locat[12][2] =
                                {
                                    {rows -1,cols/2 -1}, {rows -1,cols/2  },{rows -2,cols/2 -1},
                                    {rows -2,cols/2 },   {rows -2,cols/2 -2},{rows -2,cols/2 +1},
               
                                    {0,cols/2 -1},{0,cols/2}, {1,cols/2 -1},
                                    {1,cols/2}, {1,cols/2 -2}, {1,cols/2 +1}
                                };

    //std::vector< std::pair< Piece *,int [2][2]> > moves_chronological;
    //std::vector< std::vector<std::pair< Piece *,std::string [2]> >> afraid_trapped_safe_chronological;
    



    
    
        
};

#endif /* Generic_Board_hpp */
