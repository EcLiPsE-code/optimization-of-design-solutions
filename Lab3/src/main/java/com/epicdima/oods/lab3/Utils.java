package com.epicdima.oods.lab3;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/**
 * @author EpicDima
 */
public class Utils {
    public static final int INF = Integer.MAX_VALUE;

    public static int calculateDistance(List<Integer> nodes, int[][] c) {
        int distance = 0;
        for (int i = 0; i < nodes.size() - 1; i++) {
            distance += c[nodes.get(i)][nodes.get(i + 1)];
        }
        return distance;
    }

    public static int[][] copyArray(int[][] original, int size) {
        int[][] c = new int[size][];
        for (int i = 0; i < size; i++) {
            c[i] = Arrays.copyOf(original[i], size);
        }
        return c;
    }

    public static class Result {
        public final List<Integer> nodes;
        public final int distance;

        public Result(List<Integer> nodes, int distance) {
            this.nodes = nodes;
            this.distance = distance;
        }

        @Override
        public String toString() {
            return "Длина маршрута равна " + distance + " при прохождении через следующие точки "
                    + nodes.stream()
                    .map(it -> String.valueOf(it + 1))
                    .collect(Collectors.joining(", ", "[", "]"));
        }
    }
}
