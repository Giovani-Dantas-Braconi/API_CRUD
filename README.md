# Essa api é um exemplo simplês de API com integração de Mysql para o projeto da faculdade de ADS

# SQL para criação das tabelas utilizadas e não esquecer de baixar as libs utilizadas no projeto(requiriment.txt) 

CREATE TABLE authors (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  birthdate DATE DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


CREATE TABLE books (
  id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(100) NOT NULL,
  published_date DATE DEFAULT NULL,
  author_id INT NOT NULL,
  category_id INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (author_id) REFERENCES authors(id),
  FOREIGN KEY (category_id) REFERENCES categories(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE categories (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) COLLATE utf8mb4_general_ci,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


