CREATE DATABASE ;
USE LibraryDB;

CREATE TABLE Role (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE Branch (
    branch_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    phone VARCHAR(25),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (branch_name)
);


CREATE TABLE BranchAddress (
    branch_id INT PRIMARY KEY,
    address_line1 VARCHAR(200) NOT NULL,
    address_line2 VARCHAR(200),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100) NOT NULL DEFAULT 'Country',
    CONSTRAINT fk_branchaddress_branch FOREIGN KEY (branch_id)
        REFERENCES Branch(branch_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Publisher (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY,
    publisher_name VARCHAR(200) NOT NULL UNIQUE,
    website VARCHAR(255),
    contact_email VARCHAR(100)
);

CREATE TABLE Category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE Author (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    bio TEXT,
    UNIQUE (first_name, last_name)
);


CREATE TABLE Book (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20) UNIQUE,
    title VARCHAR(500) NOT NULL,
    subtitle VARCHAR(500),
    publisher_id INT,
    publication_year YEAR,
    language VARCHAR(50) DEFAULT 'English',
    pages INT CHECK (pages >= 0),
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_book_publisher FOREIGN KEY (publisher_id)
        REFERENCES Publisher(publisher_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_books_title (title(200))
);

CREATE TABLE BookAuthor (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    author_order SMALLINT NOT NULL DEFAULT 1, -- preserves author order
    PRIMARY KEY (book_id, author_id),
    CONSTRAINT fk_ba_book FOREIGN KEY (book_id)
        REFERENCES Book(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_ba_author FOREIGN KEY (author_id)
        REFERENCES Author(author_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE BookCategories (
    book_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (book_id, category_id),
    CONSTRAINT fk_bc_book FOREIGN KEY (book_id)
        REFERENCES Book(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_bc_category FOREIGN KEY (category_id)
        REFERENCES Category(category_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE BookCopies (
    copy_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    branch_id INT NOT NULL,
    barcode VARCHAR(100) NOT NULL UNIQUE,
    acquisition_date DATE,
    condition ENUM('NEW','GOOD','FAIR','POOR') DEFAULT 'GOOD',
    status ENUM('AVAILABLE','ON_LOAN','RESERVED','LOST','MAINTENANCE') DEFAULT 'AVAILABLE',
    location VARCHAR(100),
    CONSTRAINT fk_copy_book FOREIGN KEY (book_id)
        REFERENCES Book(book_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_copy_branch FOREIGN KEY (branch_id)
        REFERENCES Branch(branch_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    INDEX idx_copy_status (status)
);

CREATE TABLE Patron(
    patron_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    phone VARCHAR(30),
    join_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    preferred_branch_id INT,
    CONSTRAINT fk_patron_pref_branch FOREIGN KEY (preferred_branch_id)
        REFERENCES Branch(branch_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_patron_name (last_name, first_name)
);

CREATE TABLE PatronProfile (
    patron_id INT PRIMARY KEY,
    date_of_birth DATE,
    address_line1 VARCHAR(200),
    address_line2 VARCHAR(200),
    city VARCHAR(100),
    postal_code VARCHAR(20),
    membership_expires DATE,
    notes TEXT,
    CONSTRAINT fk_profile_patron FOREIGN KEY (patron_id)
        REFERENCES Patron(patron_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    role_id INT NOT NULL,
    branch_id INT,
    hired_date DATE,
    active BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_staff_role FOREIGN KEY (role_id)
        REFERENCES Role(role_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_staff_branch FOREIGN KEY (branch_id)
        REFERENCES Branch(branch_id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;


CREATE TABLE Loan (
    loan_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    copy_id BIGINT NOT NULL,
    patron_id INT NOT NULL,
    staff_issued_id INT NOT NULL,
    loan_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_date DATE NOT NULL,
    return_date DATE,
    status ENUM('ONGOING','RETURNED','OVERDUE','LOST') NOT NULL DEFAULT 'ONGOING',
    fine_amount DECIMAL(10,2) DEFAULT 0.00,
    CONSTRAINT fk_loan_copy FOREIGN KEY (copy_id)
        REFERENCES BookCopies(copy_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_loan_patron FOREIGN KEY (patron_id)
        REFERENCES Patron(patron_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_loan_staff FOREIGN KEY (staff_issued_id)
        REFERENCES Staff(staff_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_loans_patron (patron_id),
    INDEX idx_loans_copy (copy_id),
    INDEX idx_loans_status (status)
);

CREATE TABLE Fine (
    fine_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    patron_id INT NOT NULL,
    loan_id BIGINT,
    amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0),
    issued_date DATE NOT NULL DEFAULT CURRENT_DATE,
    paid BOOLEAN NOT NULL DEFAULT FALSE,
    paid_date DATE,
    reason VARCHAR(255),
    CONSTRAINT fk_fines_patron FOREIGN KEY (patron_id)
        REFERENCES Patron(patron_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_fines_loan FOREIGN KEY (loan_id)
        REFERENCES Loan(loan_id) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX idx_fines_patron (patron_id)
);

CREATE TABLE Payment (
    payment_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    fine_id BIGINT NOT NULL,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    paid_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    method ENUM('CASH','CARD','ONLINE') DEFAULT 'CASH',
    staff_id INT,
    CONSTRAINT fk_payments_fine FOREIGN KEY (fine_id)
        REFERENCES Fine(fine_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_payments_staff FOREIGN KEY (staff_id)
        REFERENCES Staff(staff_id) ON DELETE SET NULL ON UPDATE CASCADE
);


DELIMITER $$
CREATE TRIGGER trg_loans_before_insert
BEFORE INSERT ON Loans
FOR EACH ROW
BEGIN
    IF NEW.due_date < DATE(NEW.loan_date) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'due_date cannot be earlier than loan_date';
    END IF;
END$$
DELIMITER ;

-- trigger to update BookCopies.status when a loan is inserted/returned
DELIMITER $$
CREATE TRIGGER trg_loans_after_insert
AFTER INSERT ON Loans
FOR EACH ROW
BEGIN
    -- mark copy as ON_LOAN when loan created
    UPDATE BookCopies SET status = 'ON_LOAN' WHERE copy_id = NEW.copy_id;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_loans_after_update
AFTER UPDATE ON Loans
FOR EACH ROW
BEGIN
    -- if return_date set or status changed to RETURNED, mark copy as AVAILABLE
    IF NEW.status = 'RETURNED' OR (OLD.return_date IS NULL AND NEW.return_date IS NOT NULL) THEN
        UPDATE BookCopies SET status = 'AVAILABLE' WHERE copy_id = NEW.copy_id;
    END IF;

    -- if marked LOST, mark copy as LOST
    IF NEW.status = 'LOST' THEN
        UPDATE BookCopies SET status = 'LOST' WHERE copy_id = NEW.copy_id;
    END IF;
END$$
DELIMITER ;

