use pokemon;

<<<<<<< HEAD
CREATE table types(
    pokemon_id INT ,
    type VARCHAR(20) ,
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id)
);

=======
>>>>>>> cc2c49a184b36dbd984f0c1034398d8f77bfc3b9

CREATE TABLE belonging(
    owner_name VARCHAR (20) NOT NULL ,
    owner_town VARCHAR (20) NOT NULL ,
    pokemon_id INT , 
    FOREIGN KEY (owner_name,owner_town) REFERENCES owners(name,town) ON DELETE CASCADE,
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id) ON DELETE CASCADE
);
CREATE table types(
    pokemon_id INT ,
    type VARCHAR(20) ,
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(id) ON DELETE CASCADE
);
CREATE TABLE pokemon(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(20),
    type VARCHAR (20),
    hight INT,
    weight INT,
    PRIMARY KEY (id) 

);



CREATE TABLE owners(
    name VARCHAR (20) NOT NULL ,
    town VARCHAR (20) NOT NULL ,
    PRIMARY KEY (name, town) 
);










