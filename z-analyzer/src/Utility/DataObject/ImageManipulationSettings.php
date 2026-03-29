<?php

namespace App\Utility\DataObject;

use Symfony\Component\Serializer\Annotation\SerializedName;

class ImageManipulationSettings
{
    /**
     * @SerializedName("rotate_angle")
     *
     * @var int
     */
    public $rotateAngle = 0;

    /**
     * @SerializedName("crop_x")
     *
     * @var int|null
     */
    public $cropX = null;

    /**
     * @SerializedName("crop_y")
     *
     * @var int|null
     */
    public $cropY = null;

    /**
     * @SerializedName("crop_height")
     *
     * @var int|null
     */
    public $cropHeight = null;

    /**
     * @SerializedName("crop_width")
     *
     * @var int|null
     */
    public $cropWidth = null;
}
