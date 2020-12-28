package com.epicdima.oods.lab3;

import java.util.Arrays;
import java.util.stream.Collectors;

import static com.epicdima.oods.lab3.Utils.INF;

/**
 * @author EpicDima
 */
public class Main {
    public static void main(String[] args) {
//        // пример (таблица 1.1)
//        int[][] c = {
//                {INF, 30,  40,  15,  6},
//                {10,  INF, 18,  7,   9},
//                {20,  30,  INF, 1,   10},
//                {25,  10,  35,  INF, 5},
//                {9,   8,   7,   6,   INF}
//        };


//        // Задание 1 Вариант 2
//        int[][] c = {
//                {INF, 18,  25,  23,  7},
//                {3,   INF, 10,  13,  9},
//                {7,   9,   INF, 22,  10},
//                {12,  15,  24,  INF, 15},
//                {11,  9,   25,  23,  INF}
//        };

        // Задание 2 Вариант 2
        int[][] c = {
                {INF, 8,   12,  7,   5,   4,   11,  13,  9,   18,  1},
                {10,  INF, 14,  4,   7,   4,   10,  10,  6,   4,   3},
                {4,   16,  INF, 13,  3,   2,   5,   5,   5,   11,  19},
                {3,   7,   11,  INF, 7,   6,   14,  3,   3,   8,   18},
                {11,  15,  18,  12,  INF, 19,  12,  13,  15,  17,  1},
                {8,   7,   16,  19,  1,   INF, 16,  12,  11,  7,   5},
                {5,   10,  8,   6,   17,  10,  INF, 13,  9,   2,   6},
                {6,   7,   6,   5,   1,   5,   17,  INF, 14,  11,  5},
                {19,  8,   4,   19,  19,  2,   5,   14,  INF, 15,  16},
                {11,  8,   8,   3,   4,   3,   4,   11,  2,   INF, 15},
                {9,   6,   12,  3,   18,  13,  14,  3,   12,  16,  INF}
        };

//        Scanner in = new Scanner(System.in);
//
//        System.out.print("Введите размер квадратной матрицы расстояний: ");
//        int n = in.nextInt();
//
//        System.out.println("Введите расстояния (c):");
//        int[][] c = new int[n][n];
//        for (int i = 0; i < n; i++) {
//            for (int j = 0; j < n; j++) {
//                if (i == j) {
//                    c[i][j] = INF;
//                } else {
//                    System.out.print("c[" + (i + 1) + "][" + (j + 1) + "] = ");
//                    c[i][j] = in.nextInt();
//                }
//            }
//        }

        System.out.println("Матрица расстояний:");
        System.out.println(Arrays.stream(c)
                .map((arr) -> Arrays.stream(arr)
                        .mapToObj(it -> it == INF ? "inf" : String.valueOf(it))
                        .collect(Collectors.joining(", ", "[", "]")) + System.lineSeparator())
                .collect(Collectors.joining(
                        "",
                        "[" + System.lineSeparator(),
                        "]" + System.lineSeparator())));

        System.out.println("Ответ (метод ближайшего соседа): " + NearestNeighbor.calculate(c));
        System.out.println("Ответ (алгоритм Литтла (частный случай метода ветвей и границ)): " + Little.Inner.calculate(c));
    }
}
