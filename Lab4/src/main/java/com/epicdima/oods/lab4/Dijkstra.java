package com.epicdima.oods.lab4;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * @author EpicDima
 */
public class Dijkstra {
    public static final int INF = Integer.MAX_VALUE;

    public static int[] calculate(int[][] c, int start) {
        final int size = c.length;
        List<Integer> points = new ArrayList<>(size);
        int[] distances = new int[size];
        Arrays.fill(distances, INF);
        int current = 0;
        int currentIdx = start - 1;
        distances[currentIdx] = current;
        points.add(currentIdx);
        for (int i = 0; i < size - 1; i++) {
            findInRow(c, size, distances, current, currentIdx);
            findInCol(c, distances, current, currentIdx);
            current = Integer.MAX_VALUE;
            for (int j = 0; j < size; j++) {
                if (!points.contains(j) && distances[j] < current) {
                    current = distances[j];
                    currentIdx = j;
                }
            }
            points.add(currentIdx);
        }
        return distances;
    }

    private static void findInCol(int[][] c, int[] distances, int current, int currentIdx) {
        for (int j = 0; j < currentIdx; j++) {
            if (c[j][currentIdx] != INF) {
                int t = current + c[j][currentIdx];
                if (t < distances[j]) {
                    distances[j] = t;
                }
            }
        }
    }

    private static void findInRow(int[][] c, int size, int[] distances, int current, int currentIdx) {
        for (int j = currentIdx + 1; j < size; j++) {
            if (c[currentIdx][j] != INF) {
                int t = current + c[currentIdx][j];
                if (t < distances[j]) {
                    distances[j] = t;
                }
            }
        }
    }
}
