package com.epicdima.oods.lab3;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import static com.epicdima.oods.lab3.Utils.INF;

/**
 * @author EpicDima
 */
public class NearestNeighbor {
    public static Utils.Result calculate(int[][] c) {
        final int size = c.length;
        List<Integer> result = null;
        int distance = INF;
        for (int k = 0; k < size; k++) {
            List<Integer> nodes = new ArrayList<>(size);
            nodes.add(k);
            findMinInRow(c, k, nodes);
            nodes.add(k);
            int d = Utils.calculateDistance(nodes, c);
            if (d < distance) {
                distance = d;
                result = nodes;
            }
        }
        return new Utils.Result(result, distance);
    }

    private static void findMinInRow(int[][] c, int k, List<Integer> nodes) {
        int current = k;
        while (true) {
            int min = INF;
            int minIdx = -1;
            for (int i = 0; i < c[current].length; i++) {
                if (!nodes.contains(i) && c[current][i] < min) {
                    min = c[current][i];
                    minIdx = i;
                }
            }
            if (minIdx == -1) {
                break;
            }
            current = minIdx;
            nodes.add(current);
        }
    }
}
