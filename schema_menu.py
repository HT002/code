orders = [
    'SET FOREIGN_KEY_CHECKS=0',
    'DROP TABLE  IF EXISTS dia_comida',
    'DROP TABLE  IF EXISTS turno',
    'SET FOREIGN_KEY_CHECKS=1',
    """
        CREATE TABLE dia_comida (
            id INT PRIMARY KEY AUTO_INCREMENT,
            fecha DATE NOT NULL UNIQUE
        );
    """,
    """
        CREATE TABLE turno (
            id INT PRIMARY KEY AUTO_INCREMENT,
            tipo_turno VARCHAR(10) NOT NULL,
            id_dia_comida INT NOT NULL,
            FOREIGN KEY (id_dia_comida) REFERENCES dia_comida(id)
        );
    """,
    'insert into dia_comida (fecha) values (now());'
]