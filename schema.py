instructions = [
    'SET FOREIGN_KEY_CHECKS=0',
    'DROP TABLE  IF EXISTS user',
    'DROP TABLE  IF EXISTS reserva_comida',
    'DROP TABLE  IF EXISTS reserva_deporte',
    'SET FOREIGN_KEY_CHECKS=1',
    """
        CREATE TABLE user (
            id INT PRIMARY KEY AUTO_INCREMENT,
            correo varchar(50) NOT NULL UNIQUE,
            password VARCHAR(500) NOT NULL,
            id_personal INT NOT NULL UNIQUE,
            FOREIGN KEY (id_personal) REFERENCES personal(id)
        );
    """,
    """
        CREATE TABLE reserva_deporte (
            id INT PRIMARY KEY AUTO_INCREMENT,
            fecha DATETIME NOT NULL UNIQUE,
            id_user INT NOT NULL,
            id_zona INT NOT NULL,
            FOREIGN KEY (id_user) REFERENCES user(id),
            FOREIGN KEY (id_zona) REFERENCES zona(id)
        );
    """,
    """
        CREATE TABLE reserva_comida (
            id INT PRIMARY KEY AUTO_INCREMENT,
            id_user INT NOT NULL,
            id_turno INT NOT NULL,
            FOREIGN KEY (id_user) REFERENCES user(id),
            FOREIGN KEY (id_turno) REFERENCES turno(id)
        );
    """
]