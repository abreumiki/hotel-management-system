-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3308
-- Generation Time: Jun 29, 2023 at 07:43 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hotel`
--

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE `employees` (
  `employee_id` varchar(20) NOT NULL,
  `firstname` varchar(30) NOT NULL,
  `lastname` varchar(30) NOT NULL,
  `pic` varchar(500) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `position` varchar(20) NOT NULL,
  `schedule` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`employee_id`, `firstname`, `lastname`, `pic`, `username`, `password`, `position`, `schedule`, `status`) VALUES
('1', '', '', '', 'miki', 'abreu', 'Admin', 'Morning', 'Employed'),
('10', 'mg', 'b', 'C:\\Users\\user\\Desktop\\HMS_PROJECT\\640px-Technological_University_of_the_Philippines_Seal.svg-removebg-preview.png', 'mg', 'g', 'Admin', 'Night', 'Employed'),
('11', 'sol', 'abreu', 'C:\\Users\\user\\Desktop\\HMS_PROJECT\\7d27af7f38b8270e95438feb30a4b39d.jpg', 'gel', '1', 'Admin', 'Night', ''),
('12', 'Miki', 'Abreu', 'C:/Users/user/Desktop/HMS_PROJECT/marshall lee.jpg', 'mk', '1', 'Admin', 'Morning', 'Employed'),
('13', 'g', 'g', 'C:\\Users\\user\\Desktop\\HMS_PROJECT\\adventure time.jpg', 'k', 'r', 'Admin', 'Morning', 'Employed'),
('14', 'hehe', 'gagu', 'C:\\Users\\user\\Desktop\\HMS_PROJECT\\miki.jpg', '1', '1', 'Admin', 'Morning', 'Employed'),
('15', 'haha', 'haha', 'C:/Users/user/Desktop/HMS_PROJECT/ABREU, MIKI PIC.jpg', 'r', 'r', 'Admin', 'Morning', 'Employed'),
('16', 'm', 'a', 'C:/Users/user/Desktop/HMS_PROJECT/hotelB.png', 'a', 'a', 'Receptionist', 'Morning', 'Employed'),
('2', '', '', '', 'joji', '123', 'Receptionist', 'Night', 'Employed'),
('3', 'food', 'panda', 'C:/Users/user/Desktop/pkgame/en2.png', 'hakdog', '123', 'Admin', 'Morning', 'Employed'),
('5', 'Miki', 'Abreu', 'C:\\Users\\user\\Desktop\\HMS_PROJECT\\marshall lee.jpg', 'mk', '1', 'Admin', 'Morning', 'Employed'),
('6', 'meki', 'menajj', 'C:\\Users\\user\\Desktop\\HMS_PROJECT\\ABREU_PIC.jpg', 'miksu', '2', 'Admin', 'Night', 'Employed'),
('7', 'tup', 'cavite', 'C:\\Users\\user\\Desktop\\HMS_PROJECT\\640px-Technologi', 'tup', 'tup', 'Receptionist', 'Night', 'Employed'),
('8', 'ilil', 'hhm', 'C:\\Users\\user\\Desktop\\HMS_PROJECT\\ABREU, MIKI PIC.', 'nm', '1', 'Receptionist', 'Night', 'Terminated');

-- --------------------------------------------------------

--
-- Table structure for table `hotel_info`
--

CREATE TABLE `hotel_info` (
  `hotel_id` varchar(10) NOT NULL,
  `hotel_name` varchar(500) NOT NULL,
  `hotel_pic` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hotel_info`
--

INSERT INTO `hotel_info` (`hotel_id`, `hotel_name`, `hotel_pic`) VALUES
('1', 'Hotel Accommodation Management System', 'C:/Users/user/Desktop/HMS_PROJECT/hotelB.png');

-- --------------------------------------------------------

--
-- Table structure for table `promo`
--

CREATE TABLE `promo` (
  `promo_id` varchar(100) NOT NULL,
  `promo_name` varchar(200) NOT NULL,
  `value` varchar(100) NOT NULL,
  `start_date` varchar(100) NOT NULL,
  `expiry_date` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `promo`
--

INSERT INTO `promo` (`promo_id`, `promo_name`, `value`, `start_date`, `expiry_date`, `status`) VALUES
('1', '20% OFF', '10', '06/28/2023', '06/28/2023', 'Expired'),
('2', 'TRYTRY', '10', '06/29/2023', '06/29/2023', 'Active'),
('3', 'Q', '50', '06/29/2023', '06/29/2023', 'Active');

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

CREATE TABLE `rooms` (
  `room_number` varchar(3) NOT NULL,
  `room_type` varchar(20) NOT NULL,
  `room_rate` varchar(5) NOT NULL,
  `max_guest` varchar(3) NOT NULL,
  `bed` varchar(100) NOT NULL,
  `amenities` varchar(200) NOT NULL,
  `Status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`room_number`, `room_type`, `room_rate`, `max_guest`, `bed`, `amenities`, `Status`) VALUES
('1', 'Standard', '1000', '2', '1 Double Bed', 'Wifi, Pool Access', 'Available'),
('2', 'BEEMO', '5000', '10', '1 Single Bed, 1 Double Bed, 1 Queen Bed, 1 King Bed', 'HEHEH', 'Available'),
('3', 'BEEMO', '5000', '10', '1 Single Bed, 1 Double Bed, 1 Queen Bed, 1 King Bed', 'HEHEH', 'Unavailable'),
('4', 'JOLBE', '2', '2', '1 Single Bed', 'G', 'Available'),
('8', 'CONAN', '5', '1', '1 Single Bed, 2 Double Bed, 1 Queen Bed, 1 King Bed', 'WIFI', 'Available'),
('9', 'etivac', '555', '1', '1 Single Bed', 'Wifi, Pool Access, Gym, Parking, Aircon', 'Available');

-- --------------------------------------------------------

--
-- Table structure for table `room_info`
--

CREATE TABLE `room_info` (
  `type` varchar(20) NOT NULL,
  `pax` varchar(20) NOT NULL,
  `rate` varchar(20) NOT NULL,
  `bed` varchar(500) NOT NULL,
  `room_amenities` varchar(500) NOT NULL,
  `room_pic` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `room_info`
--

INSERT INTO `room_info` (`type`, `pax`, `rate`, `bed`, `room_amenities`, `room_pic`) VALUES
('etivac', '1', '555', '1 Single Bed', 'Wifi, Pool Access, Gym, Parking, Aircon', ''),
('Cavetown', '1', '12000', '1 Single Bed', 'Wifi', 'C:\\Users\\user\\Desktop\\HMS_PROJECT\\352242249_777226'),
('CONAN', '1', '5', '1 Single Bed, 2 Double Bed, 1 Queen Bed, 1 King Bed', 'WIFI', ''),
('JOLBE', '2', '2', '1 Single Bed', 'G', 'C:\\Users\\user\\Desktop\\HMS_PROJECT\\352242249_777226940732800_6236654111461440504_n.jpg'),
('DORA', '1', '5', '1 Single Bed, 1 Queen Bed', 'G', 'C:\\Users\\user\\Desktop\\HMS_PROJECT\\339919159_104562'),
('BEEMO', '10', '5000', '1 Single Bed, 1 Double Bed, 1 Queen Bed, 1 King Bed', 'HEHEH', 'C:\\Users\\user\\Desktop\\HMS_PROJECT\\ABREU_Proof of Enrollment.png');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`employee_id`);

--
-- Indexes for table `promo`
--
ALTER TABLE `promo`
  ADD PRIMARY KEY (`promo_id`);

--
-- Indexes for table `rooms`
--
ALTER TABLE `rooms`
  ADD PRIMARY KEY (`room_number`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
