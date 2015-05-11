import Data.List

knightPlace :: [Int] -> [[Int]]
knightPlace queenInput 
	| length queenInput == 0 = []
	| otherwise = map sort knightPlacements 
	where {	knightPlacements = addZeroes knightPlacementsWithOutZeroes knightPlacementsWithOutZeroes 0;
			knightPlacementsWithOutZeroes = coordsToList legalCoords listofEmptyLists;
			legalCoords = generateLegalCoords illegalCoords boardLength;
			illegalCoords = calculateAllPossibleQueenMoves queenCoords boardLength;
			queenCoords = queenInputToCoords queenInput 1;
			boardLength = length queenInput; 
			listofEmptyLists = makeListofEmptyLists [] boardLength} 


------------------------------------------------------------------------------------------------------------------------
                    --Functions used for determining legal moves (by first determining illegal moves)--
------------------------------------------------------------------------------------------------------------------------

--Given a length that cooresponds to a square board, and a list of queen coordinates (as tuples), returns a board of all possible
--coordinates that do not overlap with the possible queen moves of the given queen coordinates (as tuples).
generateLegalCoords :: [(Int, Int)] -> Int -> [(Int, Int)]
generateLegalCoords illegalCoords length = [(x,y) | x <- [1 .. length], y <- [1 .. length], (x,y) `notElem` illegalCoords]


--Generate a list of tuples combining the functions below
calculateAllPossibleQueenMoves :: [(Int, Int)] -> Int -> [(Int, Int)]
calculateAllPossibleQueenMoves queenCoords length = nub ( combine (
													map (queenDiagonals length) queenCoords ++ 
													map (queenLaterals length) queenCoords ++ 
													map (queenKnightMoves length) queenCoords ) ) 

--Generates a list of tuples that correspond to the possible diagonal movements for a given queen coordinate
queenDiagonals :: Int -> (Int,Int) -> [(Int,Int)]
queenDiagonals length (x,y) = [(x+a, y+b) | a <- [(-length) .. length], b <- [(-length) .. length], abs a == abs b,
												x+a > 0, x+a <= length, y+b > 0, y+b <= length]

--Generates a list of tuples that correspond to the possible horizontal or vertical movements for a given queen coordinate
queenLaterals :: Int -> (Int,Int) -> [(Int,Int)]
queenLaterals length (x,y) = [(x + a, y + b) | a <- [(-length) .. length], b <- [(-length) .. length], a == 0 || b == 0, 
												x+a > 0, x+a <= length, y+b > 0, y+b <= length]

--Generates a list of tuples that correspond to the possible 'knight-like' movements for a given queen coordinate
queenKnightMoves :: Int -> (Int,Int) -> [(Int,Int)]
queenKnightMoves length (x,y) = [(x+a, y+b) | a <- [-2, -1, 1, 2], b <- [-2, -1, 1, 2], abs a /= abs b,
												x+a > 0, x+a <= length, y+b > 0, y+b <= length] 


--Used to combine lists within a larger list together e.g. [[a,b,c], [d,e,f], [], [g]] -> [a,b,c,d,e,f,g]
combine :: [[t]] -> [t]
combine [] = []  
combine (x:xs) = x ++ combine xs

------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------------------------------------



------------------------------------------------------------------------------------------------------------------------
                 --Functions used for converting lists of lists to lists of tuples and back again--
------------------------------------------------------------------------------------------------------------------------

-----------------To translate from the given input to tuples

--Given the list that represents the queen coordinates as described in the project specification,
--return a list of coordinates as tuples that describes those same coordianates: e.g. [0,1,0,3,1] -> [(2,1), (4,3), (5,1)]
--The starting index should be one in this case - if it were zero for instance the result would be [0,1,0,3,1] -> [(1,1), (3,3), (4,1)]
queenInputToCoords :: [Int] -> Int -> [(Int, Int)]
queenInputToCoords [] index = []
queenInputToCoords (y:ys) index 
					| y > 0 = (index,y):queenInputToCoords ys (index + 1) 
					| otherwise = queenInputToCoords ys (index + 1)


-----------------To translate to the demanded output (from tuples)

--Given a list of coordinates (as tuples), returns a list of lists as specified in the project for output (without zeroes)
--(e.g.) [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(4,1),(5,1),(7,1),(7,7),(7,8),(8,7),(8,8)] ->
--       [[1,2,3],[1,2,3],[],[1],[1],[],[1,7,8],[7,8]]
--This function demands a list of empty lists that contains as many empty lists as the length of the board
coordsToList :: [(Int, Int)] -> [[Int]] -> [[Int]]
coordsToList [] list = list
coordsToList (x:xs) list = coordsToList xs (replaceAtIndex (fst x - 1) ((list !! (fst x - 1)) ++ [snd x]) list)

--Add zeroes to empty lists with a given list to acheive specified output , 
--e.g. [[1,2,3],[1,2,3],[],[1],[1],[],[1,7,8],[7,8]] -> [[1,2,3],[1,2,3],[0],[1],[1],[0],[1,7,8],[7,8]]
--two copies of the list of lists must be provided, and the initial index provided must be zero (addZeroes list list 0)
addZeroes :: [[Int]] -> [[Int]] -> Int -> [[Int]]
addZeroes [] list index = list
addZeroes (x:xs) list index = if length x > 0 
								then addZeroes xs list (index+1) 
								else addZeroes xs (replaceAtIndex index (0:x) list) (index+1)

--Generate a list of zero lists e.g. emptyOutputList [] 5 -> [[],[],[],[],[]]
makeListofEmptyLists :: [[Int]] -> Int -> [[Int]]
makeListofEmptyLists x length = if length > 0 then makeListofEmptyLists ([]:x) (length-1) else x

--Replaces an element at a given index of a list with a given element
replaceAtIndex :: Int -> a -> [a] -> [a]
replaceAtIndex n item ls = a ++ (item:b) where (a, (_:b)) = splitAt n ls

------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------------------------------------



























