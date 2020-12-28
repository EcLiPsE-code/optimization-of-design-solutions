package com.epicdima.oods.lab4;

import java.util.Arrays;
import java.util.Scanner;
import java.util.stream.Collectors;

import static com.epicdima.oods.lab4.Dijkstra.INF;

/**
 * @author EpicDima
 */
public class Main {
    public static void main(String[] args) {
//        // Пример
//        int[][] c = {
//                {INF, 7, 9, INF, INF, 14},
//                {0, INF, 10, 15, INF, INF},
//                {0, 0, INF, 11, INF, 2},
//                {0, 0, 0, INF, 6, INF},
//                {0, 0, 0, 0, INF, 9},
//                {0, 0, 0, 0, 0, INF}
//        };

//        // Вариант 2
//        int[][] c = {
//                {INF, 13, 3, 2, 5, 5, 5, 7, 11, INF},
//                {0, INF, 7, 6, INF, 3, 3, 8, 8, INF},
//                {0, 0, INF, 19, 12, 13, 11, 16, 1, 12},
//                {0, 0, 0, INF, 3, 16, 12, 11, INF, INF},
//                {0, 0, 0, 0, INF, 6, 13, 1, INF, INF},
//                {0, 0, 0, 0, 0, INF, 7, INF, INF, INF},
//                {0, 0, 0, 0, 0, 0, INF, 12, INF, 16},
//                {0, 0, 0, 0, 0, 0, 0, INF, 4, INF},
//                {0, 0, 0, 0, 0, 0, 0, 0, INF, 4},
//                {0, 0, 0, 0, 0, 0, 0, 0, 0, INF}
//        };

//        int start = 5;

        // Вариант 4
        int[][] c = {
                {INF, 13,  3,   2,   5,   5,   5,   7,   11,  INF},
                {0,   INF, 7,   6,   INF, 3,   3,   8,   8,   INF},
                {0,   0,   INF, 19,  12,  13,  15,  17,  1,   INF},
                {0,   0,   0,   INF, 3,   16,  12,  11,  7,   INF},
                {0,   0,   0,   0,   INF, 6,   13,  1,   2,   6},
                {0,   0,   0,   0,   0,   INF, 7,   INF, 11,  INF},
                {0,   0,   0,   0,   0,   0,   INF, 12,  15,  16},
                {0,   0,   0,   0,   0,   0,   0,   INF, 4,   INF},
                {0,   0,   0,   0,   0,   0,   0,   0,   INF, INF},
                {0,   0,   0,   0,   0,   0,   0,   0,   0,   INF}
        };

        Scanner in = new Scanner(System.in);
//
//        System.out.print("Введите количество точек: ");
//        int n = in.nextInt();
//
        System.out.print("Введите начальную точку: ");
        int start = in.nextInt();
//
//        System.out.println("Введите расстояния между точками (c):");
//        int[][] c = new int[n][n];
//        for (int i = 0; i < n; i++) {
//            for (int j = i; j < n; j++) {
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

        System.out.println("Ответ (расстояния от точки #" + start + " до всех остальных): "
                + Arrays.toString(Dijkstra.calculate(c, start)));
    }
}
