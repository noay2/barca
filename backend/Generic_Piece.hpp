
#ifndef Piece_hpp
#define Piece_hpp

#include <stdio.h>
#include <string>
#include <vector>
#include <utility>

class Piece
{
    public:
    
    
    
    
    
    Piece(std::string color, std::string type, int number, int row, int col)
    {
        this -> color      = color;
        this -> type       = type;
        this -> number     = number;
        
        this -> row = row;
        this -> col = col;
        
        this -> just_infear        = false;
        this -> infear_and_trapped = false;
        
        
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
    
    
    
    
    
    
    
    
    
    std::string                                     color                      ;
    std::string                                     type                       ;
    int                                             number                     ;
    
    int                                             row;
    int                                             col;
    
    
    bool                                            just_infear                ;
    bool                                            infear_and_trapped         ;
    




    
    
    

    
};




#endif /* Piece_hpp */
