
#ifndef Piece_hpp
#define Piece_hpp

#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <utility>

class Piece
{
    public:
    
    
    
    
    
    Piece(std::string color, std::string type, int number, int row, int col, std::string * turn, std::vector<std::vector<Piece*>> * board,
          std::vector<Piece> * Pieces)
    {
        this -> color      = color;
        this -> type       = type;
        this -> number     = number;
        
        this -> row = row;
        this -> col = col;
        
        this -> just_infear        = false;
        this -> infear_and_trapped = false;
        
        this -> turn  = turn;
        this -> board = board;
        this -> rows  = board->size();
        this -> cols  = this->board->front().size();
        this -> Pieces= Pieces;
        
        
    }
    
    
    
    
    
    
    bool scares( const Piece * other_piece) const
    {
        if (   (   ((this->type == "ELEPHANT") && (other_piece->type == "LION"))
                ||((this->type == "LION")     && (other_piece->type == "MOUSE"))
                ||((this->type == "MOUSE")    && (other_piece->type == "ELEPHANT"))
               )
            
               && this->color != other_piece->color
            )
        {return true;}
        
        
        
        else
        {return false;}
        
    }
    
    
    
    
    
    
    bool scared_of(const Piece * other_piece) const
    {
        return other_piece->scares(this);
    }
    
    
    
    std::vector<std::pair<int,int>> adjacent_squares(int & col, int & row)
    {
        std::vector<std::pair<int,int>> adjacent_squares = std::vector<std::pair<int,int>> ();
        for (int rowt = row-1; rowt != row +2; ++rowt)
        {
            for (int colt = col-1; colt!= col+2; ++colt)
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
    
    
    bool infear(int& col, int & row)
    {
        
        std::vector<std::pair<int,int>> adjacent_squares = this->adjacent_squares(col, row);
        for(auto i = adjacent_squares.begin(); i!= adjacent_squares.end(); ++i)
        {
            Piece * adjacent_piece = (*board)[i->first][i->second];
            
            
            if( adjacent_piece != nullptr && this->scared_of(adjacent_piece) )
            {return true;}
        }
        return false;
    }
    
    
    void validmoves(std::vector<std::pair<int, int>> & validmoves)
    {

        
        if ( (!this->just_infear)   )                                         //If Piece not afraid, but exists afraid piece, that is priority
        {
            for (auto i = this->Pieces->begin(); i!= this->Pieces->end(); ++i)
            {
                
                if ( i->just_infear && (i->color == this->color) )
                {return;}
            }
        }
        int rowt = this->row;
        int colt = this->col;
        
        for (int rowd = -1; rowd != 2; rowd++)                               //All 8 directions
        {
            for (int cold = -1; cold != 2; cold++)
            {
                if (!( rowd == 0 && cold == 0))
                {
                    if ( (abs(cold) == abs(rowd) && (this->type == "LION" || this->type=="ELEPHANT")) ||\
                        ((cold ==0 || rowd ==0 ) && (this->type == "MOUSE"|| this->type=="ELEPHANT"))
                        )                                                     //Piece can go direction
                    {
                        //   std::cout<<rowd<<cold<<std::endl;
                        colt +=cold;
                        rowt += rowd;
                        
                        while( (rowt >=0) && (rowt < this->rows) &&           //Piece in bounds
                              (colt >=0) && (colt < this->cols) &&
                              this->board->at(rowt)[colt] == nullptr            //Piece not colliding with other piece
                              )
                        {
                            
                            if( (!this->infear(colt, rowt)) || this->infear_and_trapped) //Checks if afraid or bypasses if infear/trapped
                            {
                                validmoves.push_back({rowt, colt});
                            }
                            colt+=cold;
                            rowt+=rowd;
                        }
                    }
                }
                colt = this->col;
                rowt = this->row;
            }
        }
    }
    
    
    void modify_fear_piece()
    {
        if (!this->infear(this->col, this->row))
        {
            this->just_infear = false;
            this->infear_and_trapped = false;
            return;
        }
        
        int rowt = this->row;
        int colt = this->col;
        
        for (int rowd = -1; rowd != 2; rowd++)                               //All 8 directions
        {
            for (int cold = -1; cold != 2; cold++)
            {
                if ( !( rowd == 0 && cold == 0))
                {
                    if ( (abs(cold) == abs(rowd) && (this->type == "LION" || this->type=="ELEPHANT")) ||\
                        ((cold ==0 || rowd ==0 ) && (this->type == "MOUSE"|| this->type=="ELEPHANT"))
                        )                                                     //Piece can go direction
                    {
                        colt +=cold;
                        rowt += rowd;
                        
                        while( (rowt >=0) && (rowt < this->rows) &&           //Piece in bounds
                              (colt >=0) && (colt < this->cols) &&
                              this->board->at(rowt)[colt] == nullptr            //Piece not colliding with other piece
                              )
                        {
                            
                            
                            if( (!this->infear(this->col, this->row))) //Checks if afraid or bypasses if infear/trapped
                            {
                                this->just_infear = true;
                                this->infear_and_trapped = false;
                                return;
                            }
                            colt+=cold;
                            rowt+=rowd;
                            
                        }
                    }
                }
                colt = this->col;
                rowt = this->row;
            }
        }
        
        this->just_infear = false;
        this->infear_and_trapped = true;
        
        
    }
    
    void fear_update()
    {
        for (auto piece = this->Pieces->begin(); piece != this->Pieces->end(); piece++)
        {
            
            if( piece->just_infear || piece->infear_and_trapped || (piece->scared_of(this)
                                                                    && abs(piece->row -this->row) <=1
                                                                    && abs(piece->col -this->col) <=1
                                                                    ))
            {
                piece-> modify_fear_piece();
            }
        }
        
    }
    
    
    std::string                                     color                      ;
    std::string                                     type                       ;
    int                                             number                     ;
    
    int                                             row;
    int                                             col;
    
    
    bool                                            just_infear                ;
    bool                                            infear_and_trapped         ;
    
    std::string *                                   turn                       ;
    std::vector<std::vector<Piece*>> *              board                      ;
    std::vector<Piece> *                            Pieces                     ;
    int                                             rows                       ;
    int                                             cols                       ;


    
    
    

    
};




#endif /* Piece_hpp */
