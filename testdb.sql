-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 27, 2022 at 02:20 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `testdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `compulsory`
--

CREATE TABLE `compulsory` (
  `c_id` int(11) NOT NULL,
  `c_name` varchar(30) NOT NULL,
  `dept_name` varchar(30) NOT NULL,
  `dept_grade` int(11) NOT NULL,
  `s_limit` int(11) NOT NULL,
  `credit` int(11) NOT NULL,
  `count` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `compulsory`
--

INSERT INTO `compulsory` (`c_id`, `c_name`, `dept_name`, `dept_grade`, `s_limit`, `credit`, `count`) VALUES
(1247, '系統程式', '資訊系', 2, 5, 3, 0),
(1248, '資料庫系統', '資訊系', 2, 3, 3, 0),
(1249, '機率與統計', '資訊系', 2, 4, 3, 0),
(3449, '國防科技', '資訊系', 2, 5, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `course time`
--

CREATE TABLE `course time` (
  `c_id` int(11) NOT NULL,
  `slot` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `course time`
--

INSERT INTO `course time` (`c_id`, `slot`) VALUES
(1245, 39),
(1245, 40),
(1247, 2),
(1247, 3),
(1247, 38),
(1248, 4),
(1248, 36),
(1248, 37),
(1249, 13),
(1249, 33),
(1249, 34),
(1260, 6),
(1260, 7),
(1260, 8),
(1261, 26),
(1261, 27),
(1261, 32),
(3025, 6),
(3025, 7),
(3025, 24),
(2764, 36),
(2764, 37),
(2790, 16),
(2790, 17),
(2812, 46),
(2812, 47),
(2921, 26),
(2921, 27),
(3449, 21),
(3449, 22);

-- --------------------------------------------------------

--
-- Table structure for table `elective`
--

CREATE TABLE `elective` (
  `c_id` int(11) NOT NULL,
  `c_name` varchar(30) NOT NULL,
  `dept_name` varchar(30) NOT NULL,
  `dept_grade` int(11) NOT NULL,
  `s_limit` int(11) NOT NULL,
  `credit` int(11) NOT NULL,
  `count` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `elective`
--

INSERT INTO `elective` (`c_id`, `c_name`, `dept_name`, `dept_grade`, `s_limit`, `credit`, `count`) VALUES
(1245, 'UNIX應用與實務', '資訊系', 2, 4, 2, 1),
(1260, '互連網路', '資訊系', 2, 3, 3, 0),
(1261, '組合數學', '資訊系', 2, 3, 3, 0),
(2764, '人生哲學', '通識', 0, 4, 2, 0),
(2790, '音樂與人生', '通識', 0, 3, 2, 0),
(2812, '莎士比亞與電影', '通識', 0, 3, 2, 0),
(2921, '水墨造型設計', '通識', 0, 4, 2, 0),
(3025, '密碼學', '資訊系', 2, 3, 3, 0),
(3598, 'UNIX應用與實務', '資訊系', 2, 4, 2, 0);

-- --------------------------------------------------------

--
-- Table structure for table `people`
--

CREATE TABLE `people` (
  `id` int(11) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `people`
--

INSERT INTO `people` (`id`, `name`, `description`) VALUES
(1, 'hj', 'Hsu, HJ'),
(2, 'help', 'Hung, Help'),
(3, 'desire', 'Chen, Desire'),
(4, 'broken', 'Yang, Broken One');

-- --------------------------------------------------------

--
-- Table structure for table `selection`
--

CREATE TABLE `selection` (
  `s_id` varchar(30) NOT NULL,
  `c_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `selection`
--

INSERT INTO `selection` (`s_id`, `c_id`) VALUES
('D0947803', 1248),
('D0947803', 1249),
('D0947803', 3449),
('D0948005', 1247),
('D0948005', 1248),
('D0948005', 1249),
('D0948005', 3449),
('D0948507', 1247),
('D0948507', 1248),
('D0948507', 1249),
('D0948507', 3449),
('D0947803', 1247);

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `s_id` varchar(30) NOT NULL,
  `s_name` varchar(30) NOT NULL,
  `dept_name` varchar(30) NOT NULL,
  `register_year` int(11) NOT NULL,
  `total_credit` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`s_id`, `s_name`, `dept_name`, `register_year`, `total_credit`) VALUES
('D0123456', '王小明', '資訊系', 2021, 0),
('D0456789', '林小美', '資訊系', 2019, 0),
('D0947803', '顏莉恬', '資訊系', 2020, 10),
('D0948005', '王瀚鍾', '資訊系', 2020, 10),
('D0948507', '吳芊汝', '資訊系', 2020, 10);

-- --------------------------------------------------------

--
-- Table structure for table `username`
--

CREATE TABLE `username` (
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `username`
--

INSERT INTO `username` (`username`, `password`) VALUES
('D0947803', 'a1234567894512'),
('D0948005', 'asdf12345678'),
('D0948507', 'qwer15789461'),
('D1234567', 'asdfgh124578');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `compulsory`
--
ALTER TABLE `compulsory`
  ADD PRIMARY KEY (`c_id`);

--
-- Indexes for table `elective`
--
ALTER TABLE `elective`
  ADD PRIMARY KEY (`c_id`);

--
-- Indexes for table `people`
--
ALTER TABLE `people`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`s_id`),
  ADD KEY `total_credit` (`total_credit`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `people`
--
ALTER TABLE `people`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
