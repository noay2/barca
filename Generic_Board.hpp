

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
        this->Pieces = std::vector<Piece>();
        this->board  = std::vector<std::vector<Piece *>> ();
      //  this->moves_chronological = std::vector< std::pair< Piece *,int [2][2]> > ();
        //this->afraid_trapped_safe_chronological = std::vector< std::vector<std::pair< Piece *,std::string [2]> >> ();
        
        
        int counter = 0;
        for (int i = 0;  i< 2; ++i)
        {
            for (int j = 0 ; j<3; ++j)
            {
                for (int k = 1; k<3; k++)
                {
                    Pieces.push_back(Piece(this->colors[i], this->types[j], k,
                                           this->initial_piece_locat[counter][0], this->initial_piece_locat[counter][1]));
                    counter +=1;
                }
            }
        }
        
        
        
        for (int i = 0; i < this->rows; ++i)
        {
            this->board.push_back(std::vector<Piece*> ());
            for (int j = 0; j < this->cols; ++j)
            {
                this->board[i].push_back(nullptr);
            }
        }
        
        for(auto piece = Pieces.begin(); piece != Pieces.end(); piece++)
        {
            this->board[piece->row][piece->col] = & *piece;

        }
        

    }
    
    std::vector<std::pair<int,int>> adjacent_squares(int & col, int & row)
    {
        std::vector<std::pair<int,int>> adjacent_squares = std::vector<std::pair<int,int>> ();
        for (int rowt = row-1; rowt != row +2; ++rowt)
        {
            for (int colt = cols-1; colt!= cols+2; ++colt)
            {
                if (rowt == row && colt == col)
                {
                    
                }
                else if( (rowt >=0) && (rowt < this->rows) &&           //Piece in bounds
                        (colt >=0) && (colt < this->cols)
                        )
                {
                    adjacent_squares.push_back({rowt, colt});
                }
            }
        }
        return adjacent_squares;
    }
    
    
    bool infear(Piece * piece,int & col, int & row)
    {
    
        std::vector<std::pair<int,int>> adjacent_squares = this->adjacent_squares(col, row);
        for(auto i = adjacent_squares.begin(); i!= adjacent_squares.end(); ++i)
        {
            Piece * adjacent_piece = this->board[i->first][i->second];
            if( adjacent_piece != nullptr && piece->scared_of(adjacent_piece) )
            {return true;}
        }
        return false;
    }
    
    
    
    
    void validmoves(std::vector<std::pair<int, int>> & validmoves, int * piece_location)
    {
        Piece * piece = this->board[piece_location[0]][piece_location[1]];
        
        if (piece == nullptr || piece->color !=  this->turn)                   //Not Piece's/NULL's move
        {
            return;
            }
        
        if ( (!piece->just_infear)   )                                         //If Piece not afraid, but exists afraid piece, that is priority
        {
            for (auto i = this->Pieces.begin(); i!= this->Pieces.end(); ++i)
            {
                if ( i->just_infear && (i->color == piece->color) )
                {return;}
            }
        }
        int rowt = piece_location[0];
        int colt = piece_location[1];
        
        for (int rowd = -1; rowd != 2; rowd++)                               //All 8 directions
        {
            for (int cold = -1; cold != 2; cold++)
            {
                if (!( rowd == 0 && cold == 0))
                {
                    if ( (abs(cold) == abs(rowd) && (piece->type == "LION" || piece->type=="ELEPHANT")) ||\
                        ((cold ==0 || rowd ==0 ) && (piece->type == "MOUSE"|| piece->type=="ELEPHANT"))
                        )                                                     //Piece can go direction
                    {
                     //   std::cout<<rowd<<cold<<std::endl;
                        colt +=cold;
                        rowt += rowd;
                        
                        while( (rowt >=0) && (rowt < this->rows) &&           //Piece in bounds
                               (colt >=0) && (colt < this->cols) &&
                                this->board[rowt][colt] == nullptr            //Piece not colliding with other piece
                             )
                        {

                            if( (!this->infear(piece, colt, rowt)) || piece->infear_and_trapped) //Checks if afraid or bypasses if infear/trapped
                            {
                                validmoves.push_back({rowt, colt});
                            }
                            colt+=cold;
                            rowt+=rowd;
                        }
                    }
                }
                colt = piece_location[1];
                rowt = piece_location[0];
            }
        }
    }
    void modify_fear_piece(Piece * piece)
    {
        if (!this->infear(piece, piece->col, piece->row))
        {
            piece->just_infear = false;
            piece->infear_and_trapped = false;
            return;
        }
        
        int rowt = piece->row;
        int colt = piece->col;
        
        for (int rowd = -1; rowd != 2; rowd++)                               //All 8 directions
        {
            for (int cold = -1; cold != 2; cold++)
            {
                if ( !(rowd == cold == 0))
                {
                    if ( (abs(cold) == abs(rowd) && (piece->type == "LION" || piece->type=="ELEPHANT")) ||\
                        ((cold ==0 || rowd ==0 ) && (piece->type == "MOUSE"|| piece->type=="ELEPHANT"))
                        )                                                     //Piece can go direction
                    {
                        colt +=cold;
                        rowt += rowd;
                        
                        while( (rowt >=0) && (rowt < this->rows) &&           //Piece in bounds
                              (colt >=0) && (colt < this->cols) &&
                              this->board[rowt][colt] == nullptr            //Piece not colliding with other piece
                              )
                        {

                            
                            if( (!this->infear(piece, colt, rowt))) //Checks if afraid or bypasses if infear/trapped
                            {
                                piece->just_infear = true;
                                piece->infear_and_trapped = false;
                                return;
                            }
                            colt+=cold;
                            rowt+=rowd;
                            
                        }
                    }
                }
                colt = piece->col;
                rowt = piece->row;
            }
        }
        
        piece->just_infear = false;
        piece->infear_and_trapped = true;
        
        
    }
    
    void fear_update(Piece * moving_piece)
    {
        for (auto piece = Pieces.begin(); piece != Pieces.end(); piece++)
        {
            
            if( piece->just_infear || piece->infear_and_trapped || (piece->scared_of(moving_piece)
                                                                && abs(piece->row -moving_piece->row) <=1
                                                                && abs(piece->col -moving_piece->col) <=1
                                                                ))
               {
                   modify_fear_piece( & *piece);
               }
        }
        
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
        
        fear_update(piece);
        
        this->check_victory();
        this->switch_turn();
        
        
    }
    
    
    

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
               

               
    bool exists_victory;
    std::string turn = "WHITE";
    
    std::vector<Piece> Pieces;
    std::vector<std::vector<Piece*>> board;
    
    //std::vector< std::pair< Piece *,int [2][2]> > moves_chronological;
    //std::vector< std::vector<std::pair< Piece *,std::string [2]> >> afraid_trapped_safe_chronological;
    



    
    
        
};

#endif /* Generic_Board_hpp */
